import SwiftUI
import AVFoundation
import Speech

struct Page5View: View {
    @ObservedObject var appState: AppState
    @State private var speechRecognizer = SFSpeechRecognizer()
    @State private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    @State private var recognitionTask: SFSpeechRecognitionTask?
    @State private var audioEngine = AVAudioEngine()
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("5")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                
                // 信纸内的文本输入框
                VStack {
                    Spacer()
                        .frame(height: geometry.size.height * 0.3)
                    
                    // 文本输入区域 - 在信纸范围内
                    ZStack(alignment: .topLeading) {
                        Rectangle()
                            .fill(Color.clear)
                            .frame(width: geometry.size.width * 0.75, height: geometry.size.height * 0.4)
                        
                        if appState.letterText.isEmpty {
                            Text("说说你最与它之间最难忘的故事吧")
                                .foregroundColor(.brown.opacity(0.5))
                                .font(.system(size: 16))
                                .padding(.horizontal, 20)
                                .padding(.top, 20)
                        }
                        
                        TextEditor(text: $appState.letterText)
                            .font(.system(size: 16))
                            .foregroundColor(.brown)
                            .background(Color.clear)
                            .padding(.horizontal, 15)
                            .padding(.top, 15)
                            .scrollContentBackground(.hidden)
                    }
                    
                    Spacer()
                }
                
                // 底部功能按钮区域
                VStack {
                    Spacer()
                    
                    HStack(spacing: geometry.size.width * 0.2) {
                        // 左下角 - 返回按钮
                        Button(action: {
                            appState.navigateToPage(4)
                        }) {
                            Circle()
                                .fill(Color.clear)
                                .frame(width: 60, height: 60)
                        }
                        
                        // 中间 - 语音输入按钮（最大的）
                        Button(action: {
                            if appState.isRecording {
                                stopRecording()
                            } else {
                                startRecording()
                            }
                        }) {
                            Circle()
                                .fill(Color.clear)
                                .frame(width: 80, height: 80)
                                .scaleEffect(appState.isRecording ? 1.2 : 1.0)
                                .animation(.easeInOut(duration: 0.3), value: appState.isRecording)
                        }
                        
                        // 右下角 - 键盘输入按钮
                        Button(action: {
                            appState.showKeyboard.toggle()
                        }) {
                            Circle()
                                .fill(Color.clear)
                                .frame(width: 60, height: 60)
                        }
                    }
                    .padding(.bottom, geometry.size.height * 0.08)
                }
                
                // 发送按钮 - 在信纸的发送区域
                VStack {
                    Spacer()
                        .frame(height: geometry.size.height * 0.77)
                    
                    Button(action: {
                        sendLetter()
                    }) {
                        Rectangle()
                            .fill(Color.clear)
                            .frame(width: 120, height: 40)
                    }
                    
                    Spacer()
                }
                
                // 发送成功提示
                if appState.letterSent {
                    ZStack {
                        Color.black.opacity(0.7)
                            .ignoresSafeArea()
                        
                        VStack {
                            Image(systemName: "checkmark.circle.fill")
                                .font(.system(size: 60))
                                .foregroundColor(.green)
                            
                            Text("信已经寄给它了～")
                                .font(.system(size: 20, weight: .medium))
                                .foregroundColor(.white)
                                .padding(.top, 20)
                        }
                        .scaleEffect(appState.letterSent ? 1.0 : 0.3)
                        .opacity(appState.letterSent ? 1.0 : 0.0)
                        .animation(.spring(response: 0.6, dampingFraction: 0.8), value: appState.letterSent)
                    }
                }
            }
        }
        .onAppear {
            requestPermissions()
        }
        .onChange(of: appState.showKeyboard) { _, show in
            // 这里可以处理键盘显示逻辑
        }
    }
    
    // MARK: - 语音识别功能
    
    private func requestPermissions() {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            DispatchQueue.main.async {
                // 处理授权结果
            }
        }
        
        AVAudioSession.sharedInstance().requestRecordPermission { granted in
            DispatchQueue.main.async {
                // 处理录音权限
            }
        }
    }
    
    private func startRecording() {
        guard let speechRecognizer = speechRecognizer, speechRecognizer.isAvailable else {
            return
        }
        
        // 停止之前的任务
        recognitionTask?.cancel()
        recognitionTask = nil
        
        // 配置音频会话
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            print("音频会话配置失败: \(error)")
            return
        }
        
        // 创建识别请求
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else {
            return
        }
        
        recognitionRequest.shouldReportPartialResults = true
        
        // 创建识别任务
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { result, error in
            if let result = result {
                DispatchQueue.main.async {
                    appState.letterText = result.bestTranscription.formattedString
                }
            }
            
            if error != nil || result?.isFinal == true {
                DispatchQueue.main.async {
                    self.stopRecording()
                }
            }
        }
        
        // 配置音频引擎
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            recognitionRequest.append(buffer)
        }
        
        audioEngine.prepare()
        
        do {
            try audioEngine.start()
            appState.isRecording = true
        } catch {
            print("音频引擎启动失败: \(error)")
        }
    }
    
    private func stopRecording() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        
        recognitionRequest?.endAudio()
        recognitionRequest = nil
        
        recognitionTask?.cancel()
        recognitionTask = nil
        
        appState.isRecording = false
    }
    
    private func sendLetter() {
        // 显示发送成功提示
        withAnimation(.spring(response: 0.6, dampingFraction: 0.8)) {
            appState.letterSent = true
        }
        
        // 3秒后跳转到第6页
        DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
            withAnimation(.easeInOut(duration: 1.0)) {
                appState.navigateToPage(6)
                appState.letterSent = false
            }
        }
    }
} 
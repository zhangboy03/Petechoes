import SwiftUI

struct Page5View: View {
    @ObservedObject var appState: AppState
    
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
                        
                        // 中间 - 语音输入按钮（最大的）- 临时禁用语音功能
                        Button(action: {
                            // 暂时禁用语音功能，避免崩溃
                            print("语音功能暂时禁用")
                        }) {
                            Circle()
                                .fill(Color.clear)
                                .frame(width: 80, height: 80)
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
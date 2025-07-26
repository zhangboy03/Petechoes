//
//  ContentView.swift
//  petechoes
//
//  Created by Barry_Zhang on 2025/7/25.
//

import SwiftUI
import PhotosUI

@available(iOS 16.0, *)
struct ContentView: View {
    @State private var currentPage = 1
    @State private var selectedItem: PhotosPickerItem? = nil
    @State private var selectedImage: UIImage? = nil
    @State private var uploadStatus = ""
    @State private var isGenerating = false
    @State private var generatedImage: UIImage? = nil
    @State private var currentWaitingMessageIndex = 0
    @State private var timer: Timer?
    
    // 后端服务器配置 - 使用Zeabur公网URL
    let backendUrl = "https://petecho.zeabur.app"
    
    // 等待消息
    let waitingMessages = [
        "稍等，毛孩子正在乱动",
        "马上就拍好啦",
        "正在调整最佳角度",
        "温馨的纪念照即将完成"
    ]
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                if currentPage == 1 {
                    // 第一页
                    Image("1")
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: geometry.size.width, height: geometry.size.height)
                        .clipped()
                        .contentShape(Rectangle()) // 确保整个区域都可以点击
                        .onTapGesture { location in
                            print("点击位置: \(location.y), 屏幕高度: \(geometry.size.height)")
                            // 检查点击位置是否在底部区域（屏幕高度的70%以下）
                            if location.y > geometry.size.height * 0.7 {
                                print("点击了房子区域，准备跳转")
                                withAnimation(.easeInOut(duration: 0.5)) {
                                    currentPage = 2
                                }
                            }
                        }
                } else if currentPage == 2 {
                    // 第二页
                    ZStack {
                        if let generatedImage = generatedImage {
                            // 显示生成的纪念照 - 保持原始比例，适配屏幕
                            Image(uiImage: generatedImage)
                                .resizable()
                                .aspectRatio(contentMode: .fit)
                                .frame(width: geometry.size.width, height: geometry.size.height)
                                .clipped()
                                .background(Color.black) // 添加黑色背景
                        } else {
                            // 默认第二页背景
                            Image("2")
                                .resizable()
                                .aspectRatio(contentMode: .fill)
                                .frame(width: geometry.size.width, height: geometry.size.height)
                                .clipped()
                        }
                        
                        // 如果没有生成图片，整个屏幕都可以触发照片选择
                        if generatedImage == nil {
                            PhotosPicker(
                                selection: $selectedItem,
                                matching: .images,
                                photoLibrary: .shared()
                            ) {
                                Rectangle()
                                    .fill(Color.clear)
                                    .frame(width: geometry.size.width, height: geometry.size.height)
                            }
                            .onChange(of: selectedItem) { newItem in
                                Task {
                                    if let newItem = newItem {
                                        if let data = try? await newItem.loadTransferable(type: Data.self) {
                                            if let uiImage = UIImage(data: data) {
                                                selectedImage = uiImage
                                                await processImage(image: uiImage)
                                            }
                                        }
                                    }
                                }
                            }
                            
                            // 状态显示
                            if !uploadStatus.isEmpty {
                                VStack {
                                    Spacer()
                                    Text(uploadStatus)
                                        .foregroundColor(.white)
                                        .font(.system(size: 14))
                                        .multilineTextAlignment(.center)
                                        .padding(.bottom, 100)
                                }
                            }
                        }
                        
                        // 返回按钮和功能按钮
                        VStack {
                            HStack {
                                Button(action: {
                                    withAnimation(.easeInOut(duration: 0.5)) {
                                        currentPage = 1
                                    }
                                }) {
                                    Image(systemName: "chevron.left")
                                        .font(.title2)
                                        .foregroundColor(.white)
                                        .padding()
                                        .background(Color.black.opacity(0.3))
                                        .clipShape(Circle())
                                }
                                .padding(.leading, 20)
                                .padding(.top, 20)
                                
                                Spacer()
                                
                                // 如果已生成图片，显示重新生成按钮
                                if generatedImage != nil {
                                    Button(action: {
                                        // 重置状态，允许重新选择照片
                                        generatedImage = nil
                                        selectedImage = nil
                                        selectedItem = nil
                                        uploadStatus = ""
                                    }) {
                                        Image(systemName: "arrow.clockwise")
                                            .font(.title2)
                                            .foregroundColor(.white)
                                            .padding()
                                            .background(Color.black.opacity(0.3))
                                            .clipShape(Circle())
                                    }
                                    .padding(.trailing, 20)
                                    .padding(.top, 20)
                                }
                            }
                            Spacer()
                        }
                        
                        // 加载指示器
                        if isGenerating {
                            ZStack {
                                Color.black.opacity(0.7)
                                    .ignoresSafeArea()
                                
                                VStack(spacing: 20) {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                        .scaleEffect(1.5)
                                    
                                    Text(waitingMessages[currentWaitingMessageIndex])
                                        .foregroundColor(.white)
                                        .font(.system(size: 18, weight: .medium))
                                        .multilineTextAlignment(.center)
                                }
                            }
                        }
                    }
                }
            }
        }
        .ignoresSafeArea()

    }
    // 处理图片上传和AI生成
    func processImage(image: UIImage) async {
        await MainActor.run {
            isGenerating = true
            uploadStatus = "正在上传图片..."
            startWaitingMessageTimer()
        }
        
        // 上传图片到后端服务器
        guard let result = await uploadImageToBackend(image: image) else {
            await MainActor.run {
                uploadStatus = "图片上传失败，请检查网络连接"
                isGenerating = false
                stopWaitingMessageTimer()
            }
            return
        }
        
        await MainActor.run {
            uploadStatus = "图片上传成功，正在生成纪念照..."
        }
        
        // 保存图片到本地
        let fileName = "pet-\(UUID().uuidString).jpg"
        saveImageLocally(image: image, fileName: fileName)
        
        // 轮询状态直到生成完成
        await pollImageGenerationStatus(imageId: result.imageId)
    }
    
    // 上传图片到后端
    func uploadImageToBackend(image: UIImage) async -> (imageId: Int, generatedImageUrl: String?)? {
        guard let imageData = image.jpegData(compressionQuality: 0.9) else {
            print("❌ 无法转换图片数据")
            return nil
        }
        
        guard let url = URL(string: "\(backendUrl)/upload") else {
            print("❌ 无效的URL")
            return nil
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        do {
            let (data, response) = try await URLSession.shared.upload(for: request, from: body)
            
            if let httpResponse = response as? HTTPURLResponse {
                print("📡 服务器响应状态码: \(httpResponse.statusCode)")
                
                if httpResponse.statusCode == 200 {
                    if let jsonResponse = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                        print("✅ 上传成功: \(jsonResponse)")
                        
                        if let imageId = jsonResponse["image_id"] as? Int {
                            let generatedImageUrl = jsonResponse["generated_image_url"] as? String
                            return (imageId: imageId, generatedImageUrl: generatedImageUrl)
                        }
                    }
                } else {
                    print("❌ 服务器错误: \(httpResponse.statusCode)")
                    if let errorData = String(data: data, encoding: .utf8) {
                        print("错误详情: \(errorData)")
                    }
                }
            }
        } catch {
            print("❌ 网络请求失败: \(error)")
        }
        
        return nil
    }
    
    // 轮询图片生成状态
    func pollImageGenerationStatus(imageId: Int) async {
        let maxAttempts = 60 // 最多等待5分钟（60次 * 5秒）
        var attempts = 0
        
        while attempts < maxAttempts {
            attempts += 1
            
            if let status = await checkImageStatus(imageId: imageId) {
                print("📊 状态检查 \(attempts): \(status.status)")
                
                if status.status == "completed" && status.hasGeneratedImage {
                    if let generatedImageUrl = status.generatedImageUrl {
                        await loadGeneratedImage(from: generatedImageUrl)
                        return
                    }
                } else if status.status == "failed" {
                    await MainActor.run {
                        uploadStatus = "图片生成失败，请重试"
                        isGenerating = false
                        stopWaitingMessageTimer()
                    }
                    return
                }
            }
            
            // 等待5秒后再次检查
            try? await Task.sleep(nanoseconds: 5_000_000_000)
        }
        
        // 超时
        await MainActor.run {
            uploadStatus = "生成超时，请重试"
            isGenerating = false
            stopWaitingMessageTimer()
        }
    }
    
    // 检查图片状态
    func checkImageStatus(imageId: Int) async -> (status: String, hasGeneratedImage: Bool, generatedImageUrl: String?)? {
        guard let url = URL(string: "\(backendUrl)/status/\(imageId)") else {
            return nil
        }
        
        do {
            let (data, response) = try await URLSession.shared.data(from: url)
            
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                if let jsonResponse = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    let status = jsonResponse["status"] as? String ?? "unknown"
                    let hasGeneratedImage = jsonResponse["has_generated_image"] as? Bool ?? false
                    let generatedImageUrl = jsonResponse["generated_image_url"] as? String
                    
                    return (status: status, hasGeneratedImage: hasGeneratedImage, generatedImageUrl: generatedImageUrl)
                }
            }
        } catch {
            print("❌ 状态检查失败: \(error)")
        }
        
        return nil
    }
    
    // 加载生成的图片
    func loadGeneratedImage(from urlString: String) async {
        guard let url = URL(string: urlString) else {
            print("❌ 无效的图片URL")
            return
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            
            if let image = UIImage(data: data) {
                await MainActor.run {
                    generatedImage = image
                    uploadStatus = "纪念照生成完成！"
                    isGenerating = false
                    stopWaitingMessageTimer()
                }
                print("✅ 成功加载生成的图片")
            }
        } catch {
            await MainActor.run {
                uploadStatus = "加载生成图片失败"
                isGenerating = false
                stopWaitingMessageTimer()
            }
            print("❌ 加载生成图片失败: \(error)")
        }
    }
    
    // 保存图片到本地
    func saveImageLocally(image: UIImage, fileName: String) {
        guard let data = image.jpegData(compressionQuality: 0.8) else { return }
        
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        let filePath = documentsPath.appendingPathComponent(fileName)
        
        do {
            try data.write(to: filePath)
            print("✅ 图片已保存到本地: \(fileName)")
        } catch {
            print("❌ 保存图片失败: \(error)")
        }
    }
    
    // 启动等待消息定时器
    func startWaitingMessageTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { _ in
            currentWaitingMessageIndex = (currentWaitingMessageIndex + 1) % waitingMessages.count
        }
    }
    
    // 停止等待消息定时器
    func stopWaitingMessageTimer() {
        timer?.invalidate()
        timer = nil
        currentWaitingMessageIndex = 0
    }
}

#Preview {
    if #available(iOS 16.0, *) {
        ContentView()
    } else {
        Text("需要iOS 16.0或更高版本")
    }
}

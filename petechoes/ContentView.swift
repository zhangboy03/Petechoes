//
//  ContentView.swift
//  petechoes
//
//  Created by Barry_Zhang on 2025/7/25.
//

import SwiftUI
import PhotosUI

// 图片选择器，支持相机和相册
struct CameraImagePicker: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    @Environment(\.presentationMode) var presentationMode
    var sourceType: UIImagePickerController.SourceType
    
    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.sourceType = sourceType
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UINavigationControllerDelegate, UIImagePickerControllerDelegate {
        let parent: CameraImagePicker
        
        init(_ parent: CameraImagePicker) {
            self.parent = parent
        }
        
        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.selectedImage = image
            }
            parent.presentationMode.wrappedValue.dismiss()
        }
        
        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.presentationMode.wrappedValue.dismiss()
        }
    }
}

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
    @State private var showNextArrow = false
    @State private var showImagePicker = false
    @State private var showCamera = false
    @State private var currentPhotoIndex = 0 // 当前选择的照片索引 (0-3)
    @State private var memoryPhotos: [UIImage?] = [nil, nil, nil, nil] // 4张记忆照片
    @State private var processedPhotos: [UIImage?] = [nil, nil, nil, nil] // AI处理后的照片
    @State private var isProcessingPhotos = false
    
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
                            ZStack {
                                Image(uiImage: generatedImage)
                                    .resizable()
                                    .aspectRatio(contentMode: .fit)
                                    .frame(width: geometry.size.width, height: geometry.size.height)
                                    .clipped()
                                    .background(Color.black) // 添加黑色背景
                                
                                // 延迟显示的下一步箭头
                                if showNextArrow {
                                    VStack {
                                        Spacer()
                                        
                                        Button(action: {
                                            withAnimation(.easeInOut(duration: 0.5)) {
                                                currentPage = 4 // 跳转到第4页
                                            }
                                        }) {
                                            HStack(spacing: 10) {
                                                Text("下一步")
                                                    .font(.system(size: 18, weight: .medium))
                                                    .foregroundColor(.white)
                                                
                                                Image(systemName: "arrow.right")
                                                    .font(.system(size: 16, weight: .medium))
                                                    .foregroundColor(.white)
                                            }
                                            .padding(.horizontal, 20)
                                            .padding(.vertical, 12)
                                            .background(Color.black.opacity(0.7))
                                            .cornerRadius(25)
                                        }
                                        .padding(.bottom, 50)
                                        .transition(.opacity.combined(with: .scale))
                                    }
                                }
                            }
                            .onAppear {
                                // 生成图片显示后，延迟3秒显示箭头
                                DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
                                    withAnimation(.easeInOut(duration: 0.8)) {
                                        showNextArrow = true
                                    }
                                }
                            }
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
                                        showNextArrow = false
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
                } else if currentPage == 5 {
                    // 第5页 - 显示图片5
                    ZStack {
                        Image("5")
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                            .frame(width: geometry.size.width, height: geometry.size.height)
                            .clipped()
                        
                        // 返回按钮
                        VStack {
                            HStack {
                                Button(action: {
                                    withAnimation(.easeInOut(duration: 0.5)) {
                                        currentPage = 4
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
                            }
                            Spacer()
                        }
                    }
                } else if currentPage == 4 {
                    // 第4页 - 记忆物品照片上传
                    GeometryReader { geo in
                        ZStack {
                            Image("4")
                                .resizable()
                                .aspectRatio(contentMode: .fill)
                                .frame(width: geo.size.width, height: geo.size.height)
                                .clipped()
                            
                            // 4个照片上传区域 - 根据背景图重新定位
                            VStack {
                                Spacer()
                                    .frame(height: geo.size.height * 0.15) // 顶部空间
                                
                                // 上面两个照片框 - 更精确定位
                                HStack {
                                    Spacer()
                                        .frame(width: geo.size.width * 0.12)
                                    
                                    PhotoUploadArea(
                                        photoIndex: 0,
                                        photo: memoryPhotos[0],
                                        isProcessing: isProcessingPhotos,
                                        onTap: {
                                            currentPhotoIndex = 0
                                            showPhotoActionSheet()
                                        }
                                    )
                                    
                                    Spacer()
                                        .frame(width: geo.size.width * 0.15)
                                    
                                    PhotoUploadArea(
                                        photoIndex: 1,
                                        photo: memoryPhotos[1],
                                        isProcessing: isProcessingPhotos,
                                        onTap: {
                                            currentPhotoIndex = 1
                                            showPhotoActionSheet()
                                        }
                                    )
                                    
                                    Spacer()
                                        .frame(width: geo.size.width * 0.12)
                                }
                                
                                Spacer()
                                    .frame(height: geo.size.height * 0.15)
                                
                                // 下面两个照片框
                                HStack {
                                    Spacer()
                                        .frame(width: geo.size.width * 0.05)
                                    
                                    PhotoUploadArea(
                                        photoIndex: 2,
                                        photo: memoryPhotos[2],
                                        isProcessing: isProcessingPhotos,
                                        onTap: {
                                            currentPhotoIndex = 2
                                            showPhotoActionSheet()
                                        }
                                    )
                                    
                                    Spacer()
                                        .frame(width: geo.size.width * 0.55)
                                    
                                    PhotoUploadArea(
                                        photoIndex: 3,
                                        photo: memoryPhotos[3],
                                        isProcessing: isProcessingPhotos,
                                        onTap: {
                                            currentPhotoIndex = 3
                                            showPhotoActionSheet()
                                        }
                                    )
                                    
                                    Spacer()
                                        .frame(width: geo.size.width * 0.05)
                                }
                                
                                Spacer()
                            }
                            
                            // 透明的"就这样吧"按钮区域 - 覆盖在背景按钮上
                            VStack {
                                Spacer()
                                
                                Button(action: {
                                    withAnimation(.easeInOut(duration: 0.5)) {
                                        currentPage = 5 // 跳转到第5页
                                    }
                                }) {
                                    // 透明按钮，覆盖背景图的按钮区域
                                    Rectangle()
                                        .fill(Color.clear)
                                        .frame(height: 60)
                                }
                                .padding(.horizontal, 40)
                                .padding(.bottom, 50)
                            }
                        }
                    }
                        
                        // 返回按钮
                        VStack {
                            HStack {
                                Button(action: {
                                    withAnimation(.easeInOut(duration: 0.5)) {
                                        currentPage = 2
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
                            }
                            Spacer()
                        }
                    }
                }
            }
        }
        .ignoresSafeArea()
        .sheet(isPresented: $showImagePicker) {
            VStack {
                HStack {
                    Button("取消") {
                        showImagePicker = false
                    }
                    .padding()
                    
                    Spacer()
                    
                    Text("选择照片")
                        .font(.headline)
                    
                    Spacer()
                    
                    Color.clear
                        .frame(width: 60)
                }
                .padding()
                
                VStack(spacing: 20) {
                    Button(action: {
                        showImagePicker = false
                        showCamera = true
                    }) {
                        HStack {
                            Image(systemName: "camera.fill")
                                .font(.title2)
                            Text("拍照")
                                .font(.title3)
                            Spacer()
                        }
                        .padding()
                        .background(Color.gray.opacity(0.1))
                        .cornerRadius(10)
                    }
                    .foregroundColor(.primary)
                    
                    PhotosPicker(
                        selection: $selectedItem,
                        matching: .images,
                        photoLibrary: .shared()
                    ) {
                        HStack {
                            Image(systemName: "photo.fill")
                                .font(.title2)
                            Text("从相册选择")
                                .font(.title3)
                            Spacer()
                        }
                        .padding()
                        .background(Color.gray.opacity(0.1))
                        .cornerRadius(10)
                    }
                    .foregroundColor(.primary)
                    .onChange(of: selectedItem) { newItem in
                        if newItem != nil {
                            showImagePicker = false
                        }
                    }
                }
                .padding()
                
                Spacer()
            }
        }
        .sheet(isPresented: $showCamera) {
            CameraImagePicker(
                selectedImage: $selectedImage,
                sourceType: .camera
            )
        }
        .onChange(of: selectedImage) { newImage in
            if let image = newImage {
                memoryPhotos[currentPhotoIndex] = image
                processMemoryPhoto(image: image, index: currentPhotoIndex)
                selectedImage = nil // 重置
            }
        }

    }
    
    // 显示照片选择弹窗
    func showPhotoActionSheet() {
        showImagePicker = true
    }
    
    // 处理记忆照片AI风格化
    func processMemoryPhoto(image: UIImage, index: Int) {
        Task {
            await MainActor.run {
                isProcessingPhotos = true
            }
            
            // 上传照片到后端
            guard let result = await uploadMemoryPhotoToBackend(image: image, index: index) else {
                await MainActor.run {
                    isProcessingPhotos = false
                }
                return
            }
            
            // 轮询AI处理结果
            await pollMemoryPhotoProcessing(imageId: result.imageId, index: index)
        }
    }
    
    // 上传记忆照片到后端
    func uploadMemoryPhotoToBackend(image: UIImage, index: Int) async -> (imageId: Int, generatedImageUrl: String?)? {
        guard let imageData = image.jpegData(compressionQuality: 0.9) else {
            print("❌ 无法转换图片数据")
            return nil
        }
        
        guard let url = URL(string: "\(backendUrl)/upload-memory-photo") else {
            print("❌ 无效的URL")
            return nil
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"memory_\(index).jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"photo_index\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(index)".data(using: .utf8)!)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        do {
            let (data, response) = try await URLSession.shared.upload(for: request, from: body)
            
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                if let jsonResponse = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    print("✅ 记忆照片上传成功: \(jsonResponse)")
                    
                    if let imageId = jsonResponse["image_id"] as? Int {
                        let generatedImageUrl = jsonResponse["generated_image_url"] as? String
                        return (imageId: imageId, generatedImageUrl: generatedImageUrl)
                    }
                }
            }
        } catch {
            print("❌ 记忆照片上传失败: \(error)")
        }
        
        return nil
    }
    
    // 轮询记忆照片处理状态
    func pollMemoryPhotoProcessing(imageId: Int, index: Int) async {
        let maxAttempts = 60
        var attempts = 0
        
        while attempts < maxAttempts {
            attempts += 1
            
            if let status = await checkImageStatus(imageId: imageId) {
                if status.status == "completed" && status.hasGeneratedImage {
                    if let generatedImageUrl = status.generatedImageUrl {
                        await loadProcessedMemoryPhoto(from: generatedImageUrl, index: index)
                        return
                    }
                } else if status.status == "failed" {
                    await MainActor.run {
                        isProcessingPhotos = false
                    }
                    return
                }
            }
            
            try? await Task.sleep(nanoseconds: 5_000_000_000)
        }
        
        await MainActor.run {
            isProcessingPhotos = false
        }
    }
    
    // 加载处理后的记忆照片
    func loadProcessedMemoryPhoto(from urlString: String, index: Int) async {
        guard let url = URL(string: urlString) else { return }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            
            if let image = UIImage(data: data) {
                await MainActor.run {
                    processedPhotos[index] = image
                    isProcessingPhotos = false
                }
                print("✅ 成功加载处理后的记忆照片 \(index)")
            }
        } catch {
            await MainActor.run {
                isProcessingPhotos = false
            }
            print("❌ 加载处理后的记忆照片失败: \(error)")
        }
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
            showNextArrow = false // 重置箭头状态，等待3秒后再显示
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

// 照片上传区域组件
struct PhotoUploadArea: View {
    let photoIndex: Int
    let photo: UIImage?
    let isProcessing: Bool
    let onTap: () -> Void
    
    var body: some View {
        ZStack {
            if let photo = photo {
                // 显示选择的照片
                Image(uiImage: photo)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: 120, height: 120)
                    .clipped()
                    .cornerRadius(8)
            } else {
                // 透明的触发区域，没有任何视觉元素
                Rectangle()
                    .fill(Color.clear)
                    .frame(width: 120, height: 120)
            }
            
            // 处理中的加载指示器
            if isProcessing {
                ZStack {
                    Color.black.opacity(0.6)
                        .frame(width: 120, height: 120)
                        .cornerRadius(8)
                    
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        .scaleEffect(1.2)
                }
            }
        }
        .onTapGesture {
            if !isProcessing {
                onTap()
            }
        }
    }
}

#Preview {
    if #available(iOS 16.0, *) {
        ContentView()
    } else {
        Text("需要iOS 16.0或更高版本")
    }
}

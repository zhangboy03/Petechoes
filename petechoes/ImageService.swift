import SwiftUI
import PhotosUI

@MainActor
class ImageService: ObservableObject {
    private let networkService = NetworkService.shared
    private var currentWaitingMessageIndex = 0
    private var timer: Timer?
    
    // 等待消息
    private let waitingMessages = [
        "稍等，毛孩子正在乱动",
        "马上就拍好啦",
        "正在调整最佳角度",
        "温馨的纪念照即将完成"
    ]
    
    // MARK: - 宠物照片生成
    
    func processPetImage(_ image: UIImage, appState: AppState) async {
        appState.isGenerating = true
        appState.uploadStatus = "正在上传图片..."
        startWaitingMessageTimer(appState: appState)
        
        // 上传图片到后端服务器
        guard let result = await networkService.uploadPetImage(image) else {
            appState.uploadStatus = "图片上传失败，请检查网络连接"
            appState.isGenerating = false
            stopWaitingMessageTimer()
            return
        }
        
        appState.uploadStatus = "图片上传成功，正在生成纪念照..."
        
        // 保存图片到本地
        saveImageLocally(image: image, fileName: "pet-\(UUID().uuidString).jpg")
        
        // 轮询状态直到生成完成
        await pollImageGenerationStatus(imageId: result.imageId, appState: appState)
    }
    
    private func pollImageGenerationStatus(imageId: Int, appState: AppState) async {
        let maxAttempts = 60
        var attempts = 0
        
        while attempts < maxAttempts && appState.isGenerating {
            attempts += 1
            
            if let status = await networkService.checkImageStatus(imageId: imageId) {
                if status.status == "completed" && status.hasGeneratedImage {
                    if let generatedImageUrl = status.generatedImageUrl {
                        await loadGeneratedImage(from: generatedImageUrl, appState: appState)
                        return
                    }
                } else if status.status == "failed" {
                    appState.uploadStatus = "图片生成失败，请重试"
                    appState.isGenerating = false
                    stopWaitingMessageTimer()
                    return
                }
            }
            
            try? await Task.sleep(nanoseconds: 5_000_000_000) // 5秒
        }
        
        // 超时处理
        appState.uploadStatus = "生成超时，请重试"
        appState.isGenerating = false
        stopWaitingMessageTimer()
    }
    
    private func loadGeneratedImage(from urlString: String, appState: AppState) async {
        if let image = await networkService.downloadImage(from: urlString) {
            appState.generatedImage = image
            appState.uploadStatus = "纪念照生成完成！"
            appState.isGenerating = false
            appState.showNextArrow = false
            stopWaitingMessageTimer()
            
            // 保存到本地
            saveImageLocally(image: image, fileName: "generated-\(UUID().uuidString).jpg")
            
            // 3秒后显示箭头
            try? await Task.sleep(nanoseconds: 3_000_000_000)
            withAnimation(.easeInOut) {
                appState.showNextArrow = true
            }
            
            print("✅ 成功加载生成的图片")
        } else {
            appState.uploadStatus = "加载生成的图片失败"
            appState.isGenerating = false
            stopWaitingMessageTimer()
        }
    }
    
    // MARK: - 记忆照片处理
    
    func processMemoryPhoto(_ image: UIImage, index: Int, appState: AppState) async {
        appState.isProcessingPhotos = true
        
        // 上传照片到后端
        guard let result = await networkService.uploadMemoryPhoto(image, index: index) else {
            appState.isProcessingPhotos = false
            return
        }
        
        // 轮询AI处理结果
        await pollMemoryPhotoProcessing(imageId: result.imageId, index: index, appState: appState)
    }
    
    private func pollMemoryPhotoProcessing(imageId: Int, index: Int, appState: AppState) async {
        let maxAttempts = 60
        var attempts = 0
        
        while attempts < maxAttempts {
            attempts += 1
            
            if let status = await networkService.checkImageStatus(imageId: imageId) {
                if status.status == "completed" && status.hasGeneratedImage {
                    if let generatedImageUrl = status.generatedImageUrl {
                        if let processedImage = await networkService.downloadImage(from: generatedImageUrl) {
                            // 这里可以存储处理后的照片，目前先不用
                            appState.isProcessingPhotos = false
                            print("✅ 成功处理记忆照片 \(index)")
                            return
                        }
                    }
                } else if status.status == "failed" {
                    appState.isProcessingPhotos = false
                    return
                }
            }
            
            try? await Task.sleep(nanoseconds: 5_000_000_000)
        }
        
        appState.isProcessingPhotos = false
    }
    
    // MARK: - 辅助方法
    
    private func saveImageLocally(image: UIImage, fileName: String) {
        guard let documentsDirectory = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first,
              let data = image.jpegData(compressionQuality: 0.9) else {
            return
        }
        
        let filePath = documentsDirectory.appendingPathComponent(fileName)
        
        do {
            try data.write(to: filePath)
            print("✅ 图片已保存到本地: \(fileName)")
        } catch {
            print("❌ 保存图片失败: \(error)")
        }
    }
    
    private func startWaitingMessageTimer(appState: AppState) {
        timer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { _ in
            Task { @MainActor in
                self.currentWaitingMessageIndex = (self.currentWaitingMessageIndex + 1) % self.waitingMessages.count
                appState.uploadStatus = self.waitingMessages[self.currentWaitingMessageIndex]
            }
        }
    }
    
    private func stopWaitingMessageTimer() {
        timer?.invalidate()
        timer = nil
        currentWaitingMessageIndex = 0
    }
} 
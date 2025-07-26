import SwiftUI
import PhotosUI

@MainActor
class AppState: ObservableObject {
    // 页面导航，0为启动页面
    @Published var currentPage: Int = 0
    
    // 图片选择状态
    @Published var selectedItem: PhotosPickerItem? = nil
    @Published var selectedImage: UIImage? = nil
    
    // 宠物照片生成相关
    @Published var uploadStatus = ""
    @Published var isGenerating = false
    @Published var generatedImage: UIImage? = nil
    @Published var showNextArrow = false
    
    // 记忆照片相关
    @Published var currentPhotoIndex = 0
    @Published var memoryPhotos: [UIImage?] = [nil, nil, nil, nil]
    @Published var isProcessingPhotos = false
    
    // 第5页信件相关
    @Published var letterText = ""
    @Published var showKeyboard = false
    @Published var letterSent = false
    
    // 导航方法
    func navigateToPage(_ page: Int) {
        withAnimation(.easeInOut(duration: 0.5)) {
            currentPage = page
        }
    }
    
    // 重置状态
    func resetPhotoGeneration() {
        generatedImage = nil
        showNextArrow = false
        uploadStatus = ""
        isGenerating = false
    }
    
    func resetMemoryPhotos() {
        memoryPhotos = [nil, nil, nil, nil]
        isProcessingPhotos = false
        currentPhotoIndex = 0
    }
} 
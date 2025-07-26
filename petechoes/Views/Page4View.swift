import SwiftUI
import PhotosUI

struct Page4View: View {
    @ObservedObject var appState: AppState
    @ObservedObject var imageService: ImageService
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("4")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                
                // 4个照片上传区域 - 左侧三张竖着排列，右下一张
                HStack {
                    // 左侧三张照片竖着排列
                    VStack(spacing: geometry.size.height * 0.08) {
                        Spacer()
                            .frame(height: geometry.size.height * 0.18)
                        
                        ForEach(0..<3, id: \.self) { index in
                            MemoryPhotoArea(
                                index: index,
                                photo: appState.memoryPhotos[index],
                                isProcessing: appState.isProcessingPhotos && appState.currentPhotoIndex == index,
                                appState: appState,
                                imageService: imageService
                            )
                        }
                        
                        Spacer()
                    }
                    .padding(.leading, geometry.size.width * 0.08)
                    
                    Spacer()
                    
                    // 右下角第四张照片
                    VStack {
                        Spacer()
                        
                        HStack {
                            Spacer()
                            
                            MemoryPhotoArea(
                                index: 3,
                                photo: appState.memoryPhotos[3],
                                isProcessing: appState.isProcessingPhotos && appState.currentPhotoIndex == 3,
                                appState: appState,
                                imageService: imageService
                            )
                        }
                        .padding(.trailing, geometry.size.width * 0.08)
                        .padding(.bottom, geometry.size.height * 0.25)
                    }
                }
                
                // 透明的"就这样吧"按钮区域
                VStack {
                    Spacer()
                    
                    Button(action: {
                        appState.navigateToPage(5)
                    }) {
                        Rectangle()
                            .fill(Color.clear)
                            .frame(height: 60)
                    }
                    .padding(.horizontal, 40)
                    .padding(.bottom, 50)
                }
                
                // 返回按钮
                VStack {
                    HStack {
                        Button(action: {
                            appState.navigateToPage(2)
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

// 记忆照片上传区域组件
struct MemoryPhotoArea: View {
    let index: Int
    let photo: UIImage?
    let isProcessing: Bool
    @ObservedObject var appState: AppState
    @ObservedObject var imageService: ImageService
    
    var body: some View {
        ZStack {
            if let photo = photo {
                Image(uiImage: photo)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: 120, height: 120)
                    .clipped()
                    .cornerRadius(8)
            } else {
                PhotosPicker(
                    selection: Binding(
                        get: { 
                            appState.currentPhotoIndex == index ? appState.selectedItem : nil 
                        },
                        set: { 
                            appState.selectedItem = $0
                            appState.currentPhotoIndex = index
                        }
                    ),
                    matching: .images,
                    photoLibrary: .shared()
                ) {
                    Rectangle()
                        .fill(Color.clear)
                        .frame(width: 120, height: 120)
                }
                .onChange(of: appState.selectedItem) { _, newItem in
                    if appState.currentPhotoIndex == index {
                        Task {
                            if let newItem = newItem {
                                if let data = try? await newItem.loadTransferable(type: Data.self) {
                                    if let uiImage = UIImage(data: data) {
                                        appState.memoryPhotos[index] = uiImage
                                        await imageService.processMemoryPhoto(uiImage, index: index, appState: appState)
                                    }
                                }
                                appState.selectedItem = nil
                            }
                        }
                    }
                }
            }
            
            if isProcessing {
                Color.black.opacity(0.6)
                    .frame(width: 120, height: 120)
                    .cornerRadius(8)
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
            }
        }
    }
} 
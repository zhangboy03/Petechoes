import SwiftUI
import PhotosUI

struct Page2View: View {
    @ObservedObject var appState: AppState
    @ObservedObject var imageService: ImageService
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("2")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                
                // 如果没有生成图片，整个屏幕都是PhotosPicker触发区域
                if appState.generatedImage == nil {
                    PhotosPicker(
                        selection: $appState.selectedItem,
                        matching: .images,
                        photoLibrary: .shared()
                    ) {
                        Rectangle()
                            .fill(Color.clear)
                            .frame(width: geometry.size.width, height: geometry.size.height)
                    }
                    .onChange(of: appState.selectedItem) { _, newItem in
                        Task {
                            if let newItem = newItem {
                                if let data = try? await newItem.loadTransferable(type: Data.self) {
                                    if let uiImage = UIImage(data: data) {
                                        appState.selectedImage = uiImage
                                        await imageService.processPetImage(uiImage, appState: appState)
                                    }
                                }
                            }
                        }
                    }
                    
                    // 状态显示
                    if !appState.uploadStatus.isEmpty {
                        VStack {
                            Spacer()
                            Text(appState.uploadStatus)
                                .foregroundColor(.white)
                                .font(.system(size: 14))
                                .multilineTextAlignment(.center)
                                .padding(.bottom, 100)
                        }
                    }
                }
                
                // 显示生成的图片
                if let generatedImage = appState.generatedImage {
                    Image(uiImage: generatedImage)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(width: geometry.size.width, height: geometry.size.height)
                        .background(Color.black)
                        .onAppear {
                            // 图片显示后3秒出现箭头
                            DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
                                withAnimation(.easeInOut) {
                                    appState.showNextArrow = true
                                }
                            }
                        }
                    
                    // 下一步箭头
                    if appState.showNextArrow {
                        VStack {
                            Spacer()
                            HStack {
                                Spacer()
                                Button(action: {
                                    appState.navigateToPage(4)
                                }) {
                                    HStack {
                                        Text("下一步")
                                            .foregroundColor(.white)
                                        Image(systemName: "arrow.right")
                                            .foregroundColor(.white)
                                    }
                                    .padding()
                                    .background(Color.black.opacity(0.7))
                                    .cornerRadius(25)
                                }
                                .padding(.trailing, 20)
                                .padding(.bottom, 50)
                            }
                        }
                    }
                }
                
                // 返回按钮和功能按钮
                VStack {
                    HStack {
                        Button(action: {
                            appState.navigateToPage(1)
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
                        
                        if appState.generatedImage != nil {
                            Button(action: {
                                appState.resetPhotoGeneration()
                            }) {
                                Text("重新生成")
                                    .foregroundColor(.white)
                                    .padding(.horizontal, 15)
                                    .padding(.vertical, 8)
                                    .background(Color.black.opacity(0.3))
                                    .cornerRadius(15)
                            }
                            .padding(.trailing, 20)
                            .padding(.top, 20)
                        }
                    }
                    Spacer()
                }
            }
        }
    }
} 
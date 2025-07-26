import SwiftUI

struct Page6View: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("6")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                
                // 建筑物点击区域 - 上方中央
                VStack {
                    Button(action: {
                        appState.navigateToPage(7)
                    }) {
                        Rectangle()
                            .fill(Color.clear)
                            .frame(width: geometry.size.width * 0.4, height: geometry.size.height * 0.3)
                    }
                    .padding(.top, geometry.size.height * 0.1)
                    
                    Spacer()
                }
                
                // 返回按钮（可选）
                VStack {
                    HStack {
                        Button(action: {
                            appState.navigateToPage(5)
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
            .gesture(
                DragGesture()
                    .onEnded { value in
                        if value.translation.width > 100 {
                            // 向右滑动，跳转到图片8
                            appState.navigateToPage(8)
                        } else if value.translation.width < -100 {
                            // 向左滑动，跳转到图片9
                            appState.navigateToPage(9)
                        }
                    }
            )
        }
    }
} 
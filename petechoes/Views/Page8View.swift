import SwiftUI

struct Page8View: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("8")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                
                // 建筑物点击区域 - 上半部分
                VStack {
                    Button(action: {
                        appState.navigateToPage(10)
                    }) {
                        Rectangle()
                            .fill(Color.clear)
                            .frame(width: geometry.size.width, height: geometry.size.height * 0.5)
                    }
                    
                    Spacer()
                }
            }
            .gesture(
                DragGesture()
                    .onEnded { value in
                        if value.translation.width > 100 {
                            // 向右滑动，跳转到图片9
                            appState.navigateToPage(9)
                        } else if value.translation.width < -100 {
                            // 向左滑动，跳转到图片6
                            appState.navigateToPage(6)
                        }
                    }
            )
        }
    }
} 
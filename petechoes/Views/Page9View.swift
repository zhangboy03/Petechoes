import SwiftUI

struct Page9View: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("9")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
            }
            .gesture(
                DragGesture()
                    .onEnded { value in
                        if value.translation.width > 100 {
                            // 向右滑动，跳转到图片6
                            appState.navigateToPage(6)
                        } else if value.translation.width < -100 {
                            // 向左滑动，跳转到图片8
                            appState.navigateToPage(8)
                        }
                    }
            )
        }
    }
} 
import SwiftUI

struct Page1View: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        GeometryReader { geometry in
            Image("1")
                .resizable()
                .aspectRatio(contentMode: .fill)
                .frame(width: geometry.size.width, height: geometry.size.height)
                .clipped()
                .contentShape(Rectangle())
                .onTapGesture { location in
                    print("点击位置: \(location.y), 屏幕高度: \(geometry.size.height)")
                    // 检查点击位置是否在底部区域（屏幕高度的70%以下）
                    if location.y > geometry.size.height * 0.7 {
                        print("点击了房子区域，准备跳转")
                        appState.navigateToPage(2)
                    }
                }
        }
    }
} 
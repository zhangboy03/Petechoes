import SwiftUI

struct Page7View: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("7")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                
                // 全屏透明点击区域，点击返回第6页
                Button(action: {
                    appState.navigateToPage(6)
                }) {
                    Rectangle()
                        .fill(Color.clear)
                        .frame(width: geometry.size.width, height: geometry.size.height)
                }
            }
        }
    }
} 
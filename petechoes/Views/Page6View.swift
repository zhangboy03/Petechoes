import SwiftUI

struct Page6View: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // 背景色
                Color.init(red: 0.96, green: 0.87, blue: 0.70) // 温馨的米色背景
                    .ignoresSafeArea()
                
                // 圆形星球图片 - 向下移动到底部中心
                Image("6")
                    .resizable()
                    .aspectRatio(contentMode: .fit) // 保持图片完整性
                    .frame(width: geometry.size.width * 1.2, height: geometry.size.width * 1.2) // 稍微放大
                    .offset(y: geometry.size.height * 0.35) // 向下移动，使圆心在屏幕底部中心
                
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
        }
    }
} 
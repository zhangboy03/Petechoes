import SwiftUI

struct Page10View: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("10")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                
                // 新的来信点击区域 - 上部分
                VStack {
                    Button(action: {
                        appState.navigateToPage(11)
                    }) {
                        Rectangle()
                            .fill(Color.clear)
                            .frame(width: geometry.size.width * 0.8, height: geometry.size.height * 0.3)
                    }
                    .padding(.top, geometry.size.height * 0.1)
                    
                    Spacer()
                }
                
                // 返回按钮
                VStack {
                    HStack {
                        Button(action: {
                            appState.navigateToPage(8)
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
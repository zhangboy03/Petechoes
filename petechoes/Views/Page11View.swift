import SwiftUI

struct Page11View: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image("11")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                
                // 返回按钮
                VStack {
                    HStack {
                        Button(action: {
                            appState.navigateToPage(10)
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
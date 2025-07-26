import SwiftUI
import AVKit
import AVFoundation

struct SplashScreenView: View {
    @ObservedObject var appState: AppState
    @State private var player: AVPlayer?
    @State private var showMainApp = false
    
    var body: some View {
        ZStack {
            Color.black
                .ignoresSafeArea()
            
            if let player = player {
                VideoPlayer(player: player)
                    .ignoresSafeArea()
                    .disabled(true) // 禁用视频控制
                    .onAppear {
                        // 监听视频播放完成
                        NotificationCenter.default.addObserver(
                            forName: .AVPlayerItemDidPlayToEndTime,
                            object: player.currentItem,
                            queue: .main
                        ) { _ in
                            showMainApp = true
                        }
                        
                        // 开始播放
                        player.play()
                    }
            } else {
                // 如果视频加载失败，显示默认启动页面
                VStack {
                    Image("1") // 使用第一页图片作为备用
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .ignoresSafeArea()
                }
                .onAppear {
                    // 如果没有视频，3秒后进入主程序
                    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                        showMainApp = true
                    }
                }
            }
        }
        .onAppear {
            setupPlayer()
        }
        .onChange(of: showMainApp) { _, show in
            if show {
                // 开始播放背景音乐
                AudioManager.shared.startBackgroundMusic()
                // 进入主程序
                appState.navigateToPage(1)
            }
        }
    }
    
    private func setupPlayer() {
        guard let path = Bundle.main.path(forResource: "startup_animation", ofType: "mov") else {
            print("找不到开机动画文件 startup_animation.mov，将显示默认启动页面")
            return
        }
        
        let url = URL(fileURLWithPath: path)
        let playerItem = AVPlayerItem(url: url)
        
        player = AVPlayer(playerItem: playerItem)
        
        // 设置视频不循环播放
        player?.actionAtItemEnd = .none
        
        // 静音播放（如果需要保持背景音乐）
        player?.isMuted = false // 设为true如果想静音播放
    }
} 
import Foundation
import AVFoundation

class AudioManager: ObservableObject {
    static let shared = AudioManager()
    private var audioPlayer: AVAudioPlayer?
    
    private init() {
        setupAudioSession()
        setupBackgroundMusic()
    }
    
    private func setupAudioSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default, options: [.mixWithOthers])
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("音频会话配置失败: \(error)")
        }
    }
    
    private func setupBackgroundMusic() {
        guard let path = Bundle.main.path(forResource: "bgm", ofType: "MP3") else {
            print("找不到背景音乐文件 bgm.MP3")
            return
        }
        
        let url = URL(fileURLWithPath: path)
        
        do {
            audioPlayer = try AVAudioPlayer(contentsOf: url)
            audioPlayer?.numberOfLoops = -1 // 无限循环
            audioPlayer?.volume = 0.3 // 设置音量为30%，作为背景音乐
            audioPlayer?.prepareToPlay()
        } catch {
            print("背景音乐初始化失败: \(error)")
        }
    }
    
    func startBackgroundMusic() {
        audioPlayer?.play()
        print("背景音乐开始播放")
    }
    
    func stopBackgroundMusic() {
        audioPlayer?.stop()
        print("背景音乐停止播放")
    }
    
    func pauseBackgroundMusic() {
        audioPlayer?.pause()
        print("背景音乐暂停")
    }
    
    func resumeBackgroundMusic() {
        audioPlayer?.play()
        print("背景音乐恢复播放")
    }
    
    func setVolume(_ volume: Float) {
        audioPlayer?.volume = volume
    }
    
    var isPlaying: Bool {
        return audioPlayer?.isPlaying ?? false
    }
} 
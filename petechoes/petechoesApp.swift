//
//  petechoesApp.swift
//  petechoes
//
//  Created by Barry_Zhang on 2025/7/25.
//

import SwiftUI

@main
struct petechoesApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    // APP启动时开始播放背景音乐
                    AudioManager.shared.startBackgroundMusic()
                }
        }
    }
}

//
//  ContentView.swift
//  petechoes
//
//  Created by Barry_Zhang on 2025/7/25.
//

import SwiftUI

@available(iOS 16.0, *)
struct ContentView: View {
    @StateObject private var appState = AppState()
    @StateObject private var imageService = ImageService()
    
    var body: some View {
        ZStack {
            switch appState.currentPage {
            case 1:
                Page1View(appState: appState)
            case 2:
                Page2View(appState: appState, imageService: imageService)
            case 4:
                Page4View(appState: appState, imageService: imageService)
            case 5:
                Page5View(appState: appState)
            case 6:
                Page6View(appState: appState)
            case 7:
                Page7View(appState: appState)
            case 8:
                Page8View(appState: appState)
            case 9:
                Page9View(appState: appState)
            case 10:
                Page10View(appState: appState)
            case 11:
                Page11View(appState: appState)
            default:
                Page1View(appState: appState)
            }
        }
        .ignoresSafeArea()
    }
}

#Preview {
    if #available(iOS 16.0, *) {
        ContentView()
    } else {
        Text("需要iOS 16.0或更高版本")
    }
}


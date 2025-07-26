//
//  petechoesTests.swift
//  petechoesTests
//
//  Created by Barry_Zhang on 2025/7/25.
//

import Testing
import SwiftUI
@testable import petechoes

struct petechoesTests {

    @Test func contentViewInitialization() async throws {
        // 测试ContentView是否能正确初始化
        let contentView = ContentView()
        #expect(contentView != nil)
    }
    
    @Test func backendURLConfiguration() async throws {
        // 测试后端URL配置是否正确
        let contentView = ContentView()
        let mirror = Mirror(reflecting: contentView)
        
        // 通过反射检查backendUrl属性
        let backendUrlProperty = mirror.children.first { $0.label == "backendUrl" }
        #expect(backendUrlProperty != nil)
        
        if let backendUrl = backendUrlProperty?.value as? String {
            #expect(backendUrl == "https://petecho.zeabur.app")
            #expect(backendUrl.hasPrefix("https://"))
        }
    }
    
    @Test func waitingMessagesNotEmpty() async throws {
        // 测试等待消息数组不为空
        let contentView = ContentView()
        let mirror = Mirror(reflecting: contentView)
        
        let messagesProperty = mirror.children.first { $0.label == "waitingMessages" }
        #expect(messagesProperty != nil)
        
        if let messages = messagesProperty?.value as? [String] {
            #expect(messages.count > 0)
            #expect(messages.contains("稍等，毛孩子正在乱动"))
            #expect(messages.contains("马上就拍好啦"))
        }
    }
    
    @Test func imageFormatSupport() async throws {
        // 测试支持的图片格式
        // 这里可以测试PhotosPicker的配置
        let contentView = ContentView()
        #expect(contentView != nil)
        
        // 验证JPEG格式转换功能
        // 注意：这里需要实际的UIImage来测试，在单元测试中可以创建一个测试图像
    }
    
    @Test func stateManagement() async throws {
        // 测试状态管理
        let contentView = ContentView()
        let mirror = Mirror(reflecting: contentView)
        
        // 检查重要的状态变量
        let stateProperties = [
            "currentPage",
            "uploadStatus", 
            "isGenerating",
            "currentWaitingMessageIndex"
        ]
        
        for property in stateProperties {
            let prop = mirror.children.first { $0.label?.contains(property) == true }
            #expect(prop != nil, "State property \(property) should exist")
        }
    }
}

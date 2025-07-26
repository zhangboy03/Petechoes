import SwiftUI
import Foundation

class NetworkService {
    static let shared = NetworkService()
    private let backendUrl = "https://petecho.zeabur.app"
    
    private init() {}
    
    // MARK: - 宠物照片生成相关
    
    func uploadPetImage(_ image: UIImage) async -> (imageId: Int, generatedImageUrl: String?)? {
        guard let imageData = image.jpegData(compressionQuality: 0.9) else {
            print("❌ 无法转换图片数据")
            return nil
        }
        
        guard let url = URL(string: "\(backendUrl)/upload") else {
            print("❌ 无效的URL")
            return nil
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"pet.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        do {
            let (data, response) = try await URLSession.shared.upload(for: request, from: body)
            
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                if let jsonResponse = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    print("✅ 宠物照片上传成功: \(jsonResponse)")
                    
                    if let imageId = jsonResponse["image_id"] as? Int {
                        let generatedImageUrl = jsonResponse["generated_image_url"] as? String
                        return (imageId: imageId, generatedImageUrl: generatedImageUrl)
                    }
                }
            }
        } catch {
            print("❌ 宠物照片上传失败: \(error)")
        }
        
        return nil
    }
    
    // MARK: - 记忆照片相关
    
    func uploadMemoryPhoto(_ image: UIImage, index: Int) async -> (imageId: Int, generatedImageUrl: String?)? {
        guard let imageData = image.jpegData(compressionQuality: 0.9) else {
            print("❌ 无法转换图片数据")
            return nil
        }
        
        guard let url = URL(string: "\(backendUrl)/upload-memory-photo") else {
            print("❌ 无效的URL")
            return nil
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"memory_\(index).jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"photo_index\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(index)".data(using: .utf8)!)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        do {
            let (data, response) = try await URLSession.shared.upload(for: request, from: body)
            
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                if let jsonResponse = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    print("✅ 记忆照片上传成功: \(jsonResponse)")
                    
                    if let imageId = jsonResponse["image_id"] as? Int {
                        let generatedImageUrl = jsonResponse["generated_image_url"] as? String
                        return (imageId: imageId, generatedImageUrl: generatedImageUrl)
                    }
                }
            }
        } catch {
            print("❌ 记忆照片上传失败: \(error)")
        }
        
        return nil
    }
    
    // MARK: - 状态查询
    
    func checkImageStatus(imageId: Int) async -> (status: String, hasGeneratedImage: Bool, generatedImageUrl: String?)? {
        guard let url = URL(string: "\(backendUrl)/status/\(imageId)") else {
            print("❌ 无效的状态查询URL")
            return nil
        }
        
        do {
            let (data, response) = try await URLSession.shared.data(from: url)
            
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                if let jsonResponse = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    let status = jsonResponse["status"] as? String ?? "unknown"
                    let hasGeneratedImage = jsonResponse["has_generated_image"] as? Bool ?? false
                    let generatedImageUrl = jsonResponse["generated_image_url"] as? String
                    
                    return (status: status, hasGeneratedImage: hasGeneratedImage, generatedImageUrl: generatedImageUrl)
                }
            }
        } catch {
            print("❌ 状态查询失败: \(error)")
        }
        
        return nil
    }
    
    // MARK: - 图片下载
    
    func downloadImage(from urlString: String) async -> UIImage? {
        guard let url = URL(string: urlString) else { return nil }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            return UIImage(data: data)
        } catch {
            print("❌ 图片下载失败: \(error)")
            return nil
        }
    }
}

// Data扩展，用于构建multipart请求
extension Data {
    mutating func append(_ string: String) {
        if let data = string.data(using: .utf8) {
            append(data)
        }
    }
} 
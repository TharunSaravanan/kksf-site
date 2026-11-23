import SwiftUI
import UIKit

/// Renders a static page (Home / Learn More / Historical Texts) exported from the website.
/// Uses UIKit's built-in HTML import into a read-only UITextView — fully offline, keeps
/// headings, styling and tappable source links.
struct HTMLPageView: UIViewRepresentable {
    let html: String

    func makeUIView(context: Context) -> UITextView {
        let tv = UITextView()
        tv.isEditable = false
        tv.isSelectable = true
        tv.backgroundColor = UIColor(red: 1.0, green: 0xFD / 255, blue: 0xF8 / 255, alpha: 1)
        tv.textContainerInset = UIEdgeInsets(top: 20, left: 16, bottom: 40, right: 16)
        tv.linkTextAttributes = [.foregroundColor: UIColor(red: 0x8A / 255, green: 0x4B / 255, blue: 0, alpha: 1)]
        tv.attributedText = Self.render(html)
        return tv
    }

    func updateUIView(_ uiView: UITextView, context: Context) {}

    static func render(_ fragment: String) -> NSAttributedString {
        let css = """
        <style>
        body { font-family: Georgia, -apple-system; font-size: 17px; color: #1f1f1f; line-height: 1.5; }
        h1 { font-size: 26px; color: #8A4B00; }
        h2 { font-size: 21px; color: #8A4B00; }
        h3, h4 { font-size: 18px; color: #8A4B00; }
        .meta, .learn-more, .src-ref { color: #6b6b6b; font-size: 14px; }
        .tamil { font-family: "Tamil Sangam MN"; }
        a { color: #8A4B00; }
        </style>
        """
        let doc = "<html><head><meta charset=\"utf-8\">\(css)</head><body>\(fragment)</body></html>"
        if let data = doc.data(using: .utf8),
           let ns = try? NSAttributedString(
               data: data,
               options: [.documentType: NSAttributedString.DocumentType.html,
                         .characterEncoding: String.Encoding.utf8.rawValue],
               documentAttributes: nil) {
            return ns
        }
        let plain = fragment.replacingOccurrences(of: "<[^>]+>", with: "", options: .regularExpression)
        return NSAttributedString(string: plain)
    }
}

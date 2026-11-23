import SwiftUI

extension Color {
    static let kuralAccent = Color(red: 0x8A / 255, green: 0x4B / 255, blue: 0x00 / 255)
    static let kuralPaper = Color(red: 0xFF / 255, green: 0xFD / 255, blue: 0xF8 / 255)
    static let kuralLine = Color(red: 0xE8 / 255, green: 0xE0 / 255, blue: 0xD2 / 255)
}

@main
struct ThirukkuralApp: App {
    @StateObject private var store = Store()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(store)
                .tint(.kuralAccent)
        }
    }
}

struct RootView: View {
    @EnvironmentObject var store: Store

    var body: some View {
        TabView {
            NavigationStack {
                HTMLPageView(html: store.data.pages.home)
                    .ignoresSafeArea(edges: .bottom)
                    .navigationTitle("Home")
                    .navigationBarTitleDisplayMode(.inline)
            }
            .tabItem { Label("Home", systemImage: "house") }

            KuralsHubView()
                .tabItem { Label("The Kurals", systemImage: "book") }

            NavigationStack {
                HTMLPageView(html: store.data.pages.learn_more)
                    .navigationTitle("Learn More")
                    .navigationBarTitleDisplayMode(.inline)
            }
            .tabItem { Label("Learn More", systemImage: "info.circle") }

            NavigationStack {
                HTMLPageView(html: store.data.pages.historical_texts)
                    .navigationTitle("Historical Texts")
                    .navigationBarTitleDisplayMode(.inline)
            }
            .tabItem { Label("Historical Texts", systemImage: "books.vertical") }
        }
    }
}

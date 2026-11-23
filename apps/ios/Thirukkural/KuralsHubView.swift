import SwiftUI

enum Route: Hashable {
    case chapter(Int)
    case kural(Int)
}

/// "The Kurals" tab: search bar, all 133 chapters grouped by the three paals,
/// each expandable to preview its kurals; tap a chapter name for its page or a kural for its full study page.
struct KuralsHubView: View {
    @EnvironmentObject var store: Store
    @State private var path = NavigationPath()
    @State private var query = ""
    @State private var expanded: Set<Int> = []

    var body: some View {
        NavigationStack(path: $path) {
            List {
                if query.trimmingCharacters(in: .whitespaces).isEmpty {
                    ForEach(store.data.paals, id: \.key) { paal in
                        Section {
                            ForEach(store.chapters(inPaal: paal.key)) { ch in
                                chapterRow(ch)
                            }
                        } header: {
                            VStack(alignment: .leading, spacing: 2) {
                                Text("\(paal.ta) · \(paal.en)").font(.headline).foregroundColor(.kuralAccent)
                                Text(paal.sub).font(.caption).foregroundColor(.secondary)
                            }
                            .textCase(nil)
                        }
                    }
                } else {
                    let results = store.search(query)
                    Section("\(results.count) result\(results.count == 1 ? "" : "s")") {
                        ForEach(results.prefix(200)) { k in
                            NavigationLink(value: Route.kural(k.n)) { kuralPreview(k) }
                        }
                    }
                }
            }
            .listStyle(.insetGrouped)
            .searchable(text: $query, prompt: "Search chapters, kurals or meanings")
            .navigationTitle("The Kurals")
            .navigationDestination(for: Route.self) { route in
                switch route {
                case .chapter(let n): ChapterView(chapterNumber: n, path: $path)
                case .kural(let n): KuralView(number: n)
                }
            }
        }
    }

    @ViewBuilder
    private func chapterRow(_ ch: Chapter) -> some View {
        DisclosureGroup(isExpanded: Binding(
            get: { expanded.contains(ch.n) },
            set: { if $0 { expanded.insert(ch.n) } else { expanded.remove(ch.n) } })) {
            ForEach(store.kurals(in: ch)) { k in
                NavigationLink(value: Route.kural(k.n)) { kuralPreview(k) }
            }
        } label: {
            Button {
                path.append(Route.chapter(ch.n))
            } label: {
                HStack(alignment: .firstTextBaseline) {
                    Text("\(ch.n)").foregroundColor(.kuralAccent).frame(width: 34, alignment: .leading)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(ch.en).font(.body.weight(.semibold)).foregroundColor(.primary)
                        Text(ch.ta).font(.subheadline).foregroundColor(.secondary)
                    }
                }
            }
            .buttonStyle(.plain)
        }
    }

    private func kuralPreview(_ k: Kural) -> some View {
        HStack(alignment: .firstTextBaseline) {
            Text("\(k.n)").font(.caption).foregroundColor(.kuralAccent).frame(width: 40, alignment: .leading)
            Text(k.ta).font(.subheadline)
        }
    }
}

/// A chapter's overview page: its names, place in the book, and its ten kurals, with previous/next chapter.
struct ChapterView: View {
    @EnvironmentObject var store: Store
    let chapterNumber: Int
    @Binding var path: NavigationPath

    var body: some View {
        if let ch = store.chapterByNumber[chapterNumber] {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(ch.en).font(.title2.weight(.bold)).foregroundColor(.kuralAccent)
                        Text("\(ch.ta) · \(ch.tr)").foregroundColor(.secondary)
                        Text("Chapter \(ch.n) of 133 · Kurals \(ch.start)–\(ch.end)").font(.caption).foregroundColor(.secondary)
                    }
                    .padding(.vertical, 4)
                }
                Section("Tap a kural for its full breakdown") {
                    ForEach(store.kurals(in: ch)) { k in
                        NavigationLink(value: Route.kural(k.n)) {
                            HStack(alignment: .firstTextBaseline) {
                                Text("\(k.n)").foregroundColor(.kuralAccent).frame(width: 40, alignment: .leading)
                                Text(k.ta)
                            }
                        }
                    }
                }
                Section {
                    HStack {
                        if ch.n > 1 {
                            Button("← Chapter \(ch.n - 1)") { path.append(Route.chapter(ch.n - 1)) }
                        }
                        Spacer()
                        if ch.n < 133 {
                            Button("Chapter \(ch.n + 1) →") { path.append(Route.chapter(ch.n + 1)) }
                        }
                    }
                    .buttonStyle(.borderless)
                }
            }
            .navigationTitle("Chapter \(ch.n)")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

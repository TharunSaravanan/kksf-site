import SwiftUI

/// The full study page for one kural — same sections and order as the website.
/// Previous / next kural and "Skip to next chapter" (always the next chapter's first kural)
/// change the shown kural in place.
struct KuralView: View {
    @EnvironmentObject var store: Store
    @State var number: Int

    var body: some View {
        if let k = store.kuralByNumber[number], let ch = store.chapterByNumber[k.chapterNumber] {
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment: .leading, spacing: 18) {
                        header(k, ch).id("top")
                        section("Meaning", k.meaning)
                        section("Elementary", k.elementary)
                        section("University", k.university)

                        sectionTitle("Through the Lens of")
                        let cites = citationIndex(k)
                        ForEach(store.data.traditions, id: \.key) { t in
                            if let x = k.x[t.key] { crossRef(t.label, x, cites) }
                        }

                        if store.data.has_real_life_example, let r = k.rle {
                            sectionTitle("Real Life Example")
                            realLife(r, cites)
                        }

                        sourcesList(cites)
                        pager(k, ch, proxy)
                    }
                    .frame(maxWidth: 700, alignment: .leading)
                    .padding()
                    .frame(maxWidth: .infinity)
                }
                .background(Color.kuralPaper)
            }
            .navigationTitle("Kural \(k.n)")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    // MARK: - Pieces

    private func header(_ k: Kural, _ ch: Chapter) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Kural \(k.n)").font(.largeTitle.weight(.bold)).foregroundColor(.kuralAccent)
            Text("\(ch.en) · \(ch.tr) · \(ch.ta)").font(.subheadline).foregroundColor(.secondary)
            Text(k.ta)
                .font(.title2.weight(.semibold))
                .multilineTextAlignment(.center)
                .frame(maxWidth: .infinity)
                .padding(.top, 8)
                .textSelection(.enabled)
            Text(k.tr)
                .font(.body.italic())
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .frame(maxWidth: .infinity)
        }
    }

    private func sectionTitle(_ title: String) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title.uppercased()).font(.caption.weight(.bold)).tracking(1.2).foregroundColor(.kuralAccent)
            Rectangle().fill(Color.kuralLine).frame(height: 1)
        }
        .padding(.top, 6)
    }

    private func section(_ title: String, _ body: String) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            sectionTitle(title)
            Text(body).font(.body).textSelection(.enabled)
        }
    }

    private func crossRef(_ label: String, _ x: CrossRef, _ cites: [String: Int]) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(label).font(.headline).foregroundColor(.kuralAccent)
            Text(x.isq ? "“\(stripQuotes(x.q))”" : stripQuotes(x.q))
                .font(x.isq ? .body.italic() : .body)
            HStack(alignment: .firstTextBaseline, spacing: 4) {
                Text("— \(x.s)").font(.footnote).foregroundColor(.secondary)
                if let i = cites[x.c] { Text("[\(i)]").font(.footnote.weight(.semibold)).foregroundColor(.kuralAccent) }
            }
            Text(x.ex)
            Text(x.tb).italic().foregroundColor(.secondary)
        }
        .textSelection(.enabled)
        .padding(.vertical, 4)
    }

    private func realLife(_ r: RealLifeExample, _ cites: [String: Int]) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(r.title).font(.headline).foregroundColor(.kuralAccent)
            Text([r.date, r.place].filter { !$0.isEmpty }.joined(separator: " · "))
                .font(.footnote.italic()).foregroundColor(.secondary)
            Text(r.event)
            Text("— Sources: " + r.c.compactMap { cites[$0].map { "[\($0)]" } }.joined(separator: " "))
                .font(.footnote).foregroundColor(.secondary)
            Text(r.ex)
            Text(r.tb).italic().foregroundColor(.secondary)
        }
        .textSelection(.enabled)
    }

    private func sourcesList(_ cites: [String: Int]) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            sectionTitle("Sources for this page")
            ForEach(cites.sorted { $0.value < $1.value }, id: \.key) { entry in
                sourceRow(entry.key, entry.value)
            }
        }
    }

    @ViewBuilder
    private func sourceRow(_ cid: String, _ i: Int) -> some View {
        let s = store.data.sources[cid]
        let by = s?.by ?? ""
        let label = "\(i). \(s?.title ?? cid)" + (by.isEmpty ? "" : " (\(by))")
        if let s, !s.url.isEmpty, let url = URL(string: s.url) {
            Link(label, destination: url).font(.footnote)
        } else {
            Text(label).font(.footnote).foregroundColor(.secondary)
        }
    }

    private func pager(_ k: Kural, _ ch: Chapter, _ proxy: ScrollViewProxy) -> some View {
        VStack(spacing: 12) {
            Rectangle().fill(Color.kuralLine).frame(height: 1)
            HStack {
                if k.n > 1 { Button("← Kural \(k.n - 1)") { go(k.n - 1, proxy) } }
                Spacer()
                if k.n < 1330 { Button("Kural \(k.n + 1) →") { go(k.n + 1, proxy) } }
            }
            HStack {
                Text(ch.en).font(.footnote).foregroundColor(.secondary)
                Spacer()
                if ch.n < 133, let next = store.chapterByNumber[ch.n + 1] {
                    Button("Skip to Next Chapter →") { go(next.start, proxy) }
                        .buttonStyle(.bordered)
                }
            }
        }
        .padding(.top, 10)
    }

    // MARK: - Helpers

    private func go(_ n: Int, _ proxy: ScrollViewProxy) {
        number = n
        withAnimation { proxy.scrollTo("top", anchor: .top) }
    }

    /// Page-local numbered citations: base Tamil-text sources first, then every source used, in reading order.
    private func citationIndex(_ k: Kural) -> [String: Int] {
        var order: [String] = []
        func add(_ c: String) { if !c.isEmpty && !order.contains(c) { order.append(c) } }
        k.src.forEach(add)
        store.data.traditions.forEach { if let x = k.x[$0.key] { add(x.c) } }
        if store.data.has_real_life_example, let r = k.rle { r.c.forEach(add) }
        return Dictionary(uniqueKeysWithValues: order.enumerated().map { ($1, $0 + 1) })
    }

    private func stripQuotes(_ s: String) -> String {
        s.trimmingCharacters(in: CharacterSet(charactersIn: "“”\" "))
    }
}

import Foundation

// Mirrors apps/build_app_data.py output (thirukkural_data.json, bundled in Resources).

struct Tradition: Codable, Hashable {
    let key: String
    let label: String
}

struct Chapter: Codable, Hashable, Identifiable {
    let n: Int
    let ta: String
    let tr: String
    let en: String
    let paal: String
    let start: Int
    let end: Int
    var id: Int { n }
}

struct Paal: Codable, Hashable {
    let key: String
    let en: String
    let ta: String
    let sub: String
}

struct CrossRef: Codable, Hashable {
    let q: String        // quote or event
    let isq: Bool        // true = verbatim quote
    let ex: String       // explanation
    let tb: String       // tie-back
    let s: String        // human-readable source
    let c: String        // citation id
}

struct RealLifeExample: Codable, Hashable {
    let title: String
    let date: String
    let place: String
    let event: String
    let ex: String
    let tb: String
    let c: [String]
}

struct Kural: Codable, Hashable, Identifiable {
    let n: Int
    let ta: String
    let tr: String
    let meaning: String
    let elementary: String
    let university: String
    let src: [String]
    let x: [String: CrossRef]
    let rle: RealLifeExample?
    var id: Int { n }
    var chapterNumber: Int { (n - 1) / 10 + 1 }
}

struct Source: Codable, Hashable {
    let title: String
    let by: String
    let publisher: String
    let url: String
    let tier: String
}

struct Pages: Codable {
    let home: String
    let learn_more: String
    let historical_texts: String
}

struct AppData: Codable {
    let generated: String
    let traditions: [Tradition]
    let has_real_life_example: Bool
    let chapters: [Chapter]
    let paals: [Paal]
    let kurals: [Kural]
    let sources: [String: Source]
    let pages: Pages
}

final class Store: ObservableObject {
    let data: AppData
    let kuralByNumber: [Int: Kural]
    let chapterByNumber: [Int: Chapter]

    init() {
        guard let url = Bundle.main.url(forResource: "thirukkural_data", withExtension: "json"),
              let raw = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode(AppData.self, from: raw) else {
            fatalError("thirukkural_data.json is missing or invalid — run apps/build_app_data.py")
        }
        data = decoded
        kuralByNumber = Dictionary(uniqueKeysWithValues: decoded.kurals.map { ($0.n, $0) })
        chapterByNumber = Dictionary(uniqueKeysWithValues: decoded.chapters.map { ($0.n, $0) })
    }

    func kurals(in chapter: Chapter) -> [Kural] {
        (chapter.start...chapter.end).compactMap { kuralByNumber[$0] }
    }

    func chapters(inPaal key: String) -> [Chapter] {
        data.chapters.filter { $0.paal == key }
    }

    /// Search across chapter names (English, Tamil, transliteration), chapter numbers,
    /// kural numbers, Tamil text, transliteration and meaning.
    func search(_ query: String) -> [Kural] {
        let q = query.trimmingCharacters(in: .whitespaces).lowercased()
        guard !q.isEmpty else { return [] }
        if let num = Int(q), let k = kuralByNumber[num] { return [k] }
        return data.kurals.filter { k in
            let ch = chapterByNumber[k.chapterNumber]
            return k.ta.lowercased().contains(q) || k.tr.lowercased().contains(q)
                || k.meaning.lowercased().contains(q)
                || (ch.map { $0.en.lowercased().contains(q) || $0.ta.contains(q) || $0.tr.lowercased().contains(q) } ?? false)
        }
    }
}

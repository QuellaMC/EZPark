import SwiftUI

@main
struct EzParkApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        TabView {
            CrowdMeterView()
                .tabItem {
                    Image(systemName: "speedometer")
                    Text("Crowd Meter")
                }
            
            FeedbackView()
                .tabItem {
                    Image(systemName: "pencil")
                    Text("Feedback")
                }
        }
    }
}

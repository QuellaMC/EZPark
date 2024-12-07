import SwiftUI

struct CrowdMeterView: View {
    @State private var availability: Double = 0.0
    @State private var errorMessage: String? = nil

    var body: some View {
        VStack {
            Text("Crowd Meter")
                .font(.largeTitle)
                .padding()

            ZStack {
                Circle()
                    .stroke(lineWidth: 20)
                    .opacity(0.3)
                    .foregroundColor(Color.gray)

                Circle()
                    .trim(from: 0.0, to: availability / 100.0)
                    .stroke(style: StrokeStyle(lineWidth: 20, lineCap: .round, lineJoin: .round))
                    .foregroundColor(availability > 70 ? .green : (availability > 30 ? .yellow : .red))
                    .rotationEffect(Angle(degrees: 270))
                    .animation(.easeInOut, value: availability)

                Text(errorMessage ?? "\(Int(availability))%")
                    .font(.title)
                    .bold()
                    .foregroundColor(errorMessage == nil ? .black : .red)
            }
            .frame(width: 150, height: 150)
            .padding()

            Button(action: fetchAvailability) {
                Text("Refresh Availability")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
        }
        .onAppear(perform: fetchAvailability)
    }

    func fetchAvailability() {
        guard let url = URL(string: "http://localhost:3000/api/crowd-level") else {
            self.errorMessage = "Invalid URL"
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    self.errorMessage = "Error: \(error.localizedDescription)"
                }
                return
            }

            guard let data = data else {
                DispatchQueue.main.async {
                    self.errorMessage = "No data received"
                }
                return
            }

            do {
                let result = try JSONDecoder().decode(CrowdLevelResponse.self, from: data)
                DispatchQueue.main.async {
                    self.availability = result.availability
                    self.errorMessage = nil
                }
            } catch {
                DispatchQueue.main.async {
                    self.errorMessage = "Failed to parse data"
                }
            }
        }.resume()
    }
}

struct CrowdLevelResponse: Codable {
    let availability: Double
}

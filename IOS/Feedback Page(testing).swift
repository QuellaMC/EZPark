import SwiftUI

struct FeedbackView: View {
    @State private var feedback: String = ""
    @State private var responseMessage: String? = nil

    var body: some View {
        VStack {
            Text("Feedback")
                .font(.largeTitle)
                .padding()

            TextField("Enter your feedback here", text: $feedback)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            Button(action: sendFeedback) {
                Text("Submit Feedback")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }

            if let responseMessage = responseMessage {
                Text(responseMessage)
                    .foregroundColor(.green)
                    .padding()
            }
        }
        .padding()
    }

    func sendFeedback() {
        guard let url = URL(string: "http://localhost:3000/api/feedback") else { return }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let feedbackData = ["feedback": feedback]
        request.httpBody = try? JSONEncoder().encode(feedbackData)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    self.responseMessage = "Error: \(error.localizedDescription)"
                }
                return
            }

            DispatchQueue.main.async {
                self.responseMessage = "Feedback submitted successfully!"
            }
        }.resume()
    }
}

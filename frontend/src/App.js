import React, { useState } from "react";

const App = () => {
    const [question, setQuestion] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setResponse("");

        try {
            // Send the question to the backend
            const res = await fetch("http://127.0.0.1:5000/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question }),
            });

            if (!res.ok) {
                throw new Error("Failed to fetch response from backend");
            }

            const data = await res.json();
            if (data.error) {
                setError(data.error);
            } else {
                setResponse(data.response);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ margin: "50px", fontFamily: "Arial, sans-serif" }}>
            <h1>Material Science Chatbot</h1>
            <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question about material science..."
                    style={{
                        width: "400px",
                        padding: "10px",
                        fontSize: "16px",
                        marginRight: "10px",
                    }}
                />
                <button
                    type="submit"
                    style={{
                        padding: "10px 20px",
                        fontSize: "16px",
                        backgroundColor: "#007BFF",
                        color: "white",
                        border: "none",
                        cursor: "pointer",
                    }}
                >
                    Ask
                </button>
            </form>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: "red" }}>Error: {error}</p>}
            {response && (
                <div style={{ marginTop: "20px" }}>
                    <h2>Response:</h2>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
};

export default App;


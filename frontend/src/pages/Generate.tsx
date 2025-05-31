import { useState } from "react";
import { api } from "../api/client";
import { CodeBlock } from "../components/CodeBlock";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export function Generate() {
    const [prompt, setPrompt] = useState("");
    const [language, setLanguage] = useState("Python");
    const [code, setCode] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const { username } = useAuth();

    const handleGenerate = async () => {
        setLoading(true);
        setError("");
        try {
            const { data } = await api.post("/generate", {
                prompt,
                language
            });
            setCode(data.code);
        } catch (err: any) {
            setError(
                err.response?.data?.error ||
                "Failed to generate code. Check authentication."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-[calc(100vh-56px)] bg-gradient-to-br from-sky-100 via-white to-blue-100 flex items-center justify-center px-4 py-8">
            <div className="bg-white backdrop-blur-md rounded-3xl shadow-2xl p-10 w-full max-w-3xl transition-all">
                <div className="mb-6 flex flex-col sm:flex-row justify-between items-center">
                    <h1 className="text-3xl font-extrabold text-blue-800 flex items-center gap-2">💡 Code Snippet Generator</h1>
                    <span className="text-gray-500 text-sm mt-2 sm:mt-0">Hi, {username}!</span>
                </div>
                <div className="space-y-4">
                    <textarea
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder="Describe the code you want..."
                        className="w-full h-28 p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 transition"
                    />
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-300 transition"
                    >
                        {["Python", "JavaScript", "Java", "C++", "Go"].map((lang) => (
                            <option key={lang} value={lang}>{lang}</option>
                        ))}
                    </select>
                    <button
                        onClick={handleGenerate}
                        disabled={loading}
                        className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
                    >
                        {loading ? "Generating..." : "Generate Code"}
                    </button>
                    {error && <div className="text-red-500 text-sm">{error}</div>}
                    {code && <CodeBlock code={code} language={language.toLowerCase()} />}
                </div>
                <div className="mt-6 text-center">
                    <Link to="/history" className="text-blue-600 hover:underline text-sm">
                        View Generation History →
                    </Link>
                </div>
            </div>
        </div>
    );
}

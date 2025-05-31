import { useEffect, useState } from "react";
import { api } from "../api/client";
import { CodeBlock } from "../components/CodeBlock";
import { Link } from "react-router-dom";

type HistoryItem = {
    code: string;
    prompt: string;
    language: string;
    created_at: string;
};

export function History() {
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        (async () => {
            setLoading(true);
            setError("");
            try {
                const { data } = await api.get("/history");
                setHistory(data);
            } catch (err: any) {
                setError(
                    err.response?.data?.detail ||
                    err.response?.data?.error ||
                    "Failed to load history."
                );
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    return (
        <div className="max-w-2xl mx-auto p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">📜 Generation History</h1>
                <Link to="/" className="text-blue-600 hover:underline text-sm">
                    ← Back to Generator
                </Link>
            </div>
            {loading && <div>Loading...</div>}
            {error && <p className="text-red-500 text-sm">{error}</p>}
            {!loading && history.length === 0 && (
                <p className="text-gray-500">No history found.</p>
            )}
            <div className="space-y-6">
                {history.map((item, idx) => (
                    <div key={idx} className="border rounded-lg p-4 bg-white">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-sm text-gray-600">
                                <b>Prompt:</b> {item.prompt}
                            </span>
                            <span className="text-xs text-gray-400">
                                {new Date(item.created_at).toLocaleString()}
                            </span>
                        </div>
                        <CodeBlock code={item.code} language={item.language.toLowerCase()} />
                    </div>
                ))}
            </div>
        </div>
    );
}

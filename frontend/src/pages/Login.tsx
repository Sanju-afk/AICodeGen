import { useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        const params = new URLSearchParams();
        params.append("username", username);
        params.append("password", password);

        try {
            const { data } = await axios.post("http://localhost:8000/token", params, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });
            login(data.access_token, username);
            navigate("/");
        } catch (err: any) {
            setError(
                err.response?.data?.detail ||
                err.response?.data?.error ||
                "Invalid username or password"
            );
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200 px-4">
            <div className="max-w-md w-full space-y-6 p-10 bg-white rounded-2xl shadow-xl">
                <h2 className="text-3xl font-extrabold text-center text-gray-900">
                    Sign in to <span className="text-blue-600">CodeGen</span>
                </h2>

                <form className="mt-6 space-y-5" onSubmit={handleSubmit}>
                    {error && (
                        <div className="text-red-600 text-sm font-medium bg-red-100 border border-red-300 p-2 rounded">
                            {error}
                        </div>
                    )}

                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-1">
                            Username
                        </label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-1">
                            Password
                        </label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full flex justify-center items-center py-3 px-4 rounded-lg text-white font-semibold bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-md transition"
                    >
                        Sign in
                    </button>
                </form>
            </div>
        </div>
    );
};

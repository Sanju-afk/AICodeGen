// src/components/Navbar.tsx
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export function Navbar() {
    const { isAuthenticated, username, logout } = useAuth();

    return (
        <nav className="bg-white border-b shadow-sm py-3 px-6 flex justify-between items-center">
            <Link to="/" className="text-xl font-bold text-blue-600">CodeGen</Link>
            <div className="flex items-center gap-4">
                {isAuthenticated ? (
                    <>
                        <Link to="/history" className="text-gray-700 hover:text-blue-600">History</Link>
                        <span className="text-gray-500 text-sm">Hi, {username}!</span>
                        <button
                            onClick={logout}
                            className="bg-blue-100 text-blue-700 px-3 py-1 rounded hover:bg-blue-200 text-sm"
                        >
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="text-gray-700 hover:text-blue-600">Login</Link>
                        <Link to="/register" className="text-gray-700 hover:text-blue-600">Register</Link>
                    </>
                )}
            </div>
        </nav>
    );
}

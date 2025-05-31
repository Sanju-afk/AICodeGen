import { createContext, useContext, useEffect, useState } from "react";

type AuthContextType = {
    token: string | null;
    username: string | null;
    login: (token: string, username: string) => void;
    logout: () => void;
    isAuthenticated: boolean;
};

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [token, setToken] = useState<string | null>(null);
    const [username, setUsername] = useState<string | null>(null);

    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        const storedUsername = localStorage.getItem("username");
        if (storedToken) setToken(storedToken);
        if (storedUsername) setUsername(storedUsername);
    }, []);

    const login = (newToken: string, newUsername: string) => {
        localStorage.setItem("token", newToken);
        localStorage.setItem("username", newUsername);
        setToken(newToken);
        setUsername(newUsername);
    };

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setToken(null);
        setUsername(null);
    };

    return (
        <AuthContext.Provider
            value={{
                token,
                username,    // <-- Provide username here
                login,
                logout,
                isAuthenticated: !!token,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};


export const useAuth = () => useContext(AuthContext);
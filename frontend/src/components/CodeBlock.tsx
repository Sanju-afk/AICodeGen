interface CodeBlockProps {
    code: string;
    language: string;
}

export const CodeBlock = ({ code, language }: CodeBlockProps) => (
    <div className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto">
        <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-400">{language}</span>
            <button
                onClick={() => navigator.clipboard.writeText(code)}
                className="text-xs bg-gray-700 px-2 py-1 rounded hover:bg-gray-600"
            >
                Copy
            </button>
        </div>
        <pre className="text-sm">
            <code>{code}</code>
        </pre>
    </div>
);

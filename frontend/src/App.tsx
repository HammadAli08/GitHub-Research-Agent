import React, { useState } from 'react'
import axios from 'axios'
import { Search, Loader2, BarChart3, ShieldAlert, Code2, Users, MessageSquare, ChevronRight, XCircle, RotateCcw, AlertTriangle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface Repo {
    full_name: string
    description: string
    stars: number
    forks: number
    language: string
    url: string
}

interface Report {
    executive_summary: string
    technical_assessment: string
    risk_score: number
    tech_stack: string[]
    architecture_patterns: string[]
    maintenance_quality: string
    key_findings: string[]
    recent_activity_summary: string
    // Extended fields if needed
}

export default function App() {
    const [query, setQuery] = useState('')
    const [repos, setRepos] = useState<Repo[]>([])
    const [loading, setLoading] = useState(false)
    const [analyzing, setAnalyzing] = useState(false)
    const [selectedRepo, setSelectedRepo] = useState<string | null>(null)
    const [report, setReport] = useState<Report | null>(null)
    const [chatQuery, setChatQuery] = useState('')
    const [chatHistory, setChatHistory] = useState<{ role: string, content: string }[]>([])
    const [chatLoading, setChatLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!query) return
        setLoading(true)
        setError(null)
        try {
            const res = await axios.post('/api/search', { query })
            setRepos(res.data.repositories)
            if (res.data.repositories.length === 0) {
                setError("No repositories found for this query.")
            }
        } catch (err: any) {
            console.error(err)
            setError(err.response?.data?.detail || "Failed to fetch repositories. Please check your connection.")
        } finally {
            setLoading(false)
        }
    }

    const handleAnalyze = async (fullName: string) => {
        setSelectedRepo(fullName)
        setAnalyzing(true)
        setReport(null)
        setChatHistory([])
        setError(null)
        try {
            const res = await axios.post('/api/analyze', { repo_full_name: fullName })
            setReport(res.data)
        } catch (err: any) {
            console.error(err)
            setError(err.response?.data?.detail || "Research failed. The repository might be private or the agent timed out.")
        } finally {
            setAnalyzing(false)
        }
    }

    const handleChat = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!chatQuery || !selectedRepo) return
        const userMsg = { role: 'user', content: chatQuery }
        setChatHistory([...chatHistory, userMsg])
        setChatQuery('')
        setChatLoading(true)
        setError(null)
        try {
            const res = await axios.post('/api/chat', {
                repo_full_name: selectedRepo,
                query: chatQuery,
                history: chatHistory
            })
            setChatHistory(prev => [...prev, { role: 'assistant', content: res.data.answer }])
        } catch (err: any) {
            console.error(err)
            setError("Failed to get a response from the research assistant.")
        } finally {
            setChatLoading(false)
        }
    }

    const resetSession = () => {
        setQuery('')
        setRepos([])
        setSelectedRepo(null)
        setReport(null)
        setChatHistory([])
        setError(null)
    }

    return (
        <div className="flex h-screen bg-teal-dark text-white selection:bg-seafoam selection:text-white">
            {/* Left Sidebar: Search & Discovery */}
            <div className="w-1/3 border-r border-white/10 flex flex-col bg-black/20 backdrop-blur-md">
                <div className="p-6 border-b border-white/10">
                    <div className="flex justify-between items-center mb-4">
                        <h1 className="text-xl font-bold tracking-tighter uppercase text-seafoam">GitHub Intelligence</h1>
                        {(repos.length > 0 || selectedRepo) && (
                            <button
                                onClick={resetSession}
                                className="p-2 hover:bg-white/10 transition-colors rounded-full"
                                title="Reset Session"
                            >
                                <RotateCcw className="w-4 h-4" />
                            </button>
                        )}
                    </div>
                    <form onSubmit={handleSearch} className="relative">
                        <input
                            type="text"
                            className="w-full bg-black/20 border border-white/10 p-3 pl-10 focus:outline-none focus:border-seafoam focus:ring-1 focus:ring-seafoam placeholder:text-white/40 font-mono text-sm transition-all text-white"
                            placeholder="SEARCH REPOS..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <Search className="absolute left-3 top-3.5 w-4 h-4 text-seafoam" />
                        {loading && <Loader2 className="absolute right-3 top-3.5 w-4 h-4 animate-spin text-seafoam" />}
                    </form>
                    {error && !analyzing && !report && (
                        <div className="mt-4 p-3 bg-white/50 backdrop-blur-sm border border-black flex items-start gap-2 text-xs font-mono uppercase">
                            <AlertTriangle className="w-4 h-4 shrink-0 text-accent-primary" />
                            <span>{error}</span>
                        </div>
                    )}
                </div>

                <div className="flex-1 overflow-y-auto">
                    {repos.map((repo) => (
                        <button
                            key={repo.full_name}
                            onClick={() => handleAnalyze(repo.full_name)}
                            className={`w-full text-left p-6 border-b border-white/5 transition-all group ${selectedRepo === repo.full_name ? 'bg-seafoam/10 border-l-4 border-l-seafoam shadow-lg' : 'hover:bg-white/5'}`}
                        >
                            <div className="flex justify-between items-start mb-2">
                                <span className={`font-bold font-mono text-sm uppercase truncate ${selectedRepo === repo.full_name ? 'text-seafoam' : 'text-white'}`}>{repo.full_name}</span>
                                <ChevronRight className={`w-4 h-4 ${selectedRepo === repo.full_name ? 'text-seafoam' : 'opacity-0 group-hover:opacity-100 text-white/50'} transition-all`} />
                            </div>
                            <p className="text-xs text-white/60 line-clamp-2 mb-3 leading-relaxed">{repo.description}</p>
                            <div className="flex gap-4 text-[10px] font-mono uppercase text-white/40">
                                <span className="flex items-center gap-1"><span className="text-seafoam">★</span> {repo.stars}</span>
                                <span className="flex items-center gap-1"><span className="text-seafoam">⑂</span> {repo.forks}</span>
                                <span className="px-1.5 py-0.5 bg-white/5 border border-white/10 rounded">{repo.language}</span>
                            </div>
                        </button>
                    ))}
                    {!loading && repos.length === 0 && !query && (
                        <div className="p-12 text-center text-neutral-300 font-mono text-[10px] uppercase">
                            Input a topic or repo name above
                        </div>
                    )}
                </div>
            </div>

            {/* Right Content: Analysis & Report */}
            <div className="flex-1 overflow-y-auto p-12 relative scroll-smooth">
                {error && (analyzing || report) && (
                    <div className="fixed top-6 right-6 z-50 p-4 bg-black text-white border border-white flex items-center gap-4 animate-in slide-in-from-top duration-300">
                        <AlertTriangle className="w-5 h-5 text-neutral-400" />
                        <span className="text-sm font-mono uppercase">{error}</span>
                        <button onClick={() => setError(null)}><XCircle className="w-4 h-4" /></button>
                    </div>
                )}

                {!selectedRepo && (
                    <div className="h-full flex flex-col items-center justify-center text-neutral-400">
                        <BarChart3 className="w-12 h-12 mb-4 stroke-1" />
                        <p className="font-mono text-xs uppercase tracking-widest">Select a repository to begin analysis</p>
                    </div>
                )}

                {analyzing && (
                    <div className="h-full flex flex-col items-center justify-center">
                        <Loader2 className="w-8 h-8 animate-spin mb-4" />
                        <p className="font-mono text-xs uppercase tracking-widest animate-pulse">Running live multi-agent research...</p>
                        <p className="mt-4 text-[10px] text-neutral-400 font-mono uppercase">Analyzing structure, issues, and risks</p>
                    </div>
                )}

                {report && (
                    <div className="max-w-3xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
                        <header className="border-b border-white/10 pb-8">
                            <div className="flex justify-between items-end mb-4">
                                <div>
                                    <span className="text-[10px] font-mono text-seafoam uppercase tracking-widest block mb-1">Intelligence Report</span>
                                    <h2 className="text-4xl font-bold tracking-tighter uppercase text-white">{selectedRepo?.split('/')[1]}</h2>
                                </div>
                                <div className="text-right">
                                    <span className="block text-[10px] font-mono text-white/60 uppercase mb-1">Risk Assessment</span>
                                    <span className={`text-4xl font-bold font-mono ${report.risk_score > 70 ? 'text-red-400' : report.risk_score > 40 ? 'text-orange-300' : 'text-seafoam'}`}>
                                        {report.risk_score}<span className="text-xl text-white/40"> / 100</span>
                                    </span>
                                </div>
                            </div>
                            <p className="text-lg leading-relaxed text-white/90">{report.executive_summary}</p>
                        </header>

                        <div className="grid grid-cols-2 gap-8">
                            <section className="report-section bg-white/5 p-6 rounded-lg border border-white/5">
                                <h3 className="font-mono text-xs font-bold uppercase tracking-widest mb-4 flex items-center gap-2 text-seafoam">
                                    <Code2 className="w-4 h-4" /> Tech Stack
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                    {report.tech_stack.map(tech => (
                                        <span key={tech} className="px-2 py-1 bg-black/40 text-white text-[10px] font-mono uppercase rounded border border-white/10">{tech}</span>
                                    ))}
                                </div>
                            </section>
                            <section className="report-section bg-white/5 p-6 rounded-lg border border-white/5">
                                <h3 className="font-mono text-xs font-bold uppercase tracking-widest mb-4 flex items-center gap-2 text-seafoam">
                                    <ShieldAlert className="w-4 h-4" /> Patterns
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                    {report.architecture_patterns.map(pattern => (
                                        <span key={pattern} className="px-2 py-1 bg-seafoam/20 text-seafoam text-[10px] font-mono uppercase rounded border border-seafoam/30">{pattern}</span>
                                    ))}
                                </div>
                            </section>
                        </div>

                        <section className="report-section">
                            <h3 className="font-mono text-xs font-bold uppercase tracking-widest mb-4 flex items-center gap-2 text-seafoam">
                                <Code2 className="w-4 h-4" /> Technical Assessment
                            </h3>
                            <div className="prose prose-sm prose-invert max-w-none border-l-2 border-seafoam/20 pl-6">
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>{report.technical_assessment}</ReactMarkdown>
                            </div>
                        </section>

                        <div className="grid grid-cols-2 gap-12">
                            <section className="report-section">
                                <h3 className="font-mono text-xs font-bold uppercase tracking-widest mb-4 flex items-center gap-2">
                                    <Users className="w-4 h-4" /> Maintenance
                                </h3>
                                <p className="text-sm leading-relaxed">{report.maintenance_quality}</p>
                            </section>
                            <section className="report-section">
                                <h3 className="font-mono text-xs font-bold uppercase tracking-widest mb-4 flex items-center gap-2">
                                    <BarChart3 className="w-4 h-4" /> Activity
                                </h3>
                                <p className="text-sm leading-relaxed">{report.recent_activity_summary}</p>
                            </section>
                        </div>

                        <section className="report-section">
                            <h3 className="font-mono text-xs font-bold uppercase tracking-widest mb-4 flex items-center gap-2 text-seafoam">
                                <ShieldAlert className="w-4 h-4" /> Key Findings
                            </h3>
                            <ul className="grid grid-cols-1 gap-4">
                                {report.key_findings.map((finding, i) => (
                                    <li key={i} className="flex gap-4 items-start p-4 bg-white/5 border border-white/5 hover:bg-white/10 transition-colors rounded-lg group">
                                        <span className="font-mono text-xs text-seafoam/50 mt-0.5 group-hover:text-seafoam transition-colors">0{i + 1}</span>
                                        <span className="text-sm leading-snug text-white/80">{finding}</span>
                                    </li>
                                ))}
                            </ul>
                        </section>

                        {/* Post-Analysis Chat */}
                        <section className="mt-24 pt-12 border-t border-white/10 pb-24 -mx-12 px-12 bg-gradient-to-b from-transparent to-black/20">
                            <h3 className="font-mono text-xs font-bold uppercase tracking-widest mb-6 flex items-center gap-2 text-seafoam">
                                <MessageSquare className="w-4 h-4 text-seafoam" /> Interrogate Analysis
                            </h3>
                            <div className="space-y-6 mb-8">
                                {chatHistory.map((msg, i) => (
                                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                        <div className={`max-w-[85%] p-5 text-sm shadow-xl rounded-2xl ${msg.role === 'user'
                                            ? 'bg-seafoam text-white font-mono rounded-br-none'
                                            : 'bg-black/40 border border-white/10 text-white rounded-bl-none'
                                            }`}>
                                            <div className={`prose prose-sm max-w-none prose-invert`}>
                                                <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                                {chatLoading && (
                                    <div className="flex justify-start">
                                        <div className="bg-black/40 p-4 rounded-xl animate-pulse border border-white/5">
                                            <Loader2 className="w-4 h-4 animate-spin text-seafoam" />
                                        </div>
                                    </div>
                                )}
                            </div>
                            <form onSubmit={handleChat} className="flex gap-2">
                                <input
                                    type="text"
                                    className="flex-1 bg-black/20 border border-white/10 p-4 focus:outline-none focus:border-seafoam placeholder:text-white/40 font-mono text-sm rounded-xl transition-all text-white"
                                    placeholder="INTERROGATE RESEARCH..."
                                    value={chatQuery}
                                    onChange={(e) => setChatQuery(e.target.value)}
                                    disabled={chatLoading}
                                />
                                <button
                                    type="submit"
                                    disabled={chatLoading}
                                    className="bg-seafoam text-white px-8 py-2 uppercase font-mono text-xs font-bold hover:bg-seafoam/80 transition-all disabled:opacity-50 rounded-xl shadow-lg shadow-seafoam/20"
                                >
                                    SND
                                </button>
                            </form>
                        </section>
                    </div>
                )}
            </div>
        </div>
    )
}

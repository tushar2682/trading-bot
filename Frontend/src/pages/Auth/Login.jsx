import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../../services/api';
import { ShieldCheck, Globe, ArrowRight, Lock, User, CheckCircle2 } from 'lucide-react';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await authService.login({ email, password });
            localStorage.setItem('token', res.data.access_token);
            navigate('/');
        } catch (err) {
            alert("Operational Security Halt: Credential Mismatch Detected.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#f8fafc] flex flex-col items-center justify-center p-6 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]">
            <div className="max-w-[480px] w-full animate-biz">
                <div className="flex flex-col items-center mb-10 text-center">
                    <div className="w-20 h-20 bg-blue-600 rounded-[28px] flex items-center justify-center mb-6 shadow-2xl shadow-blue-500/20 ring-4 ring-white">
                        <Globe className="text-white" size={32} />
                    </div>
                    <h1 className="text-4xl font-bold tracking-tight text-slate-900 font-heading leading-tight">Elite Trading Terminal</h1>
                    <p className="text-slate-500 font-medium mt-3 text-lg leading-relaxed px-10">Access corporate-grade market analytics and autonomous execution.</p>
                </div>

                <div className="biz-card p-12 bg-white/90 backdrop-blur-md shadow-2xl shadow-slate-200/60 border-slate-200/80">
                    <div className="flex items-center gap-2 mb-8 p-3 bg-blue-50 rounded-xl border border-blue-100">
                        <ShieldCheck className="text-blue-600" size={18} />
                        <span className="text-[11px] font-bold text-blue-700 uppercase tracking-widest">TLS 1.3 Secure Session Connection</span>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-8">
                        <div className="space-y-2">
                            <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Professional Identity</label>
                            <div className="relative group">
                                <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-600 transition-colors" size={20} />
                                <input
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full bg-slate-50 border border-slate-200 pl-12 pr-4 py-4 rounded-xl text-slate-900 outline-none focus:ring-4 focus:ring-blue-500/5 focus:border-blue-500/50 font-semibold text-[15px] transition-all"
                                    placeholder="E.g. operator@nebu-corp.com"
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Security PIN / Password</label>
                            <div className="relative group">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-600 transition-colors" size={20} />
                                <input
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full bg-slate-50 border border-slate-200 pl-12 pr-4 py-4 rounded-xl text-slate-900 outline-none focus:ring-4 focus:ring-blue-500/5 focus:border-blue-500/50 font-semibold text-[15px] transition-all"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full h-16 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-bold uppercase tracking-[0.2em] shadow-2xl shadow-blue-500/20 transition-all active:scale-[0.98] flex items-center justify-center gap-3"
                        >
                            {loading ? 'Validating Protocols...' : 'Establish Session'}
                            {!loading && <ArrowRight size={20} className="mt-0.5" />}
                        </button>
                    </form>

                    <div className="mt-12 pt-8 border-t border-slate-100/50 text-center">
                        <p className="text-[11px] font-bold text-slate-400 uppercase tracking-widest">
                            Unauthorized Access? <Link to="/register" className="text-blue-600 hover:text-blue-700 font-extrabold underline underline-offset-4">Provision New ID</Link>
                        </p>
                    </div>
                </div>

                <div className="mt-10 grid grid-cols-2 gap-4">
                    {[
                        { label: 'Latency', value: '12ms Response', icon: CheckCircle2 },
                        { label: 'Security', value: 'FIPS 140-2 Valid', icon: ShieldCheck }
                    ].map((item, i) => (
                        <div key={i} className="flex flex-col items-center p-4 bg-white/40 rounded-2xl border border-slate-100">
                            <item.icon size={16} className="text-slate-400 mb-2" />
                            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter mb-0.5">{item.label}</p>
                            <p className="text-[11px] font-bold text-slate-700 uppercase">{item.value}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Login;

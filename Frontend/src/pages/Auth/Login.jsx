import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../../services/api';
import {
    ShieldCheck,
    Globe,
    ArrowRight,
    Lock,
    User,
    CheckCircle2,
    Cpu,
    Key
} from 'lucide-react';

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
            console.error("Login failed", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden">
            <div className="max-w-[480px] w-full relative z-10">
                {/* Brand Logo */}
                <div className="flex flex-col items-center mb-12 text-center">
                    <div className="w-24 h-24 bg-primary bg-opacity-10 rounded-[2rem] flex items-center justify-center mb-8 border border-primary border-opacity-20 shadow-2xl shadow-primary/20 backdrop-blur-xl">
                        <Cpu className="text-primary" size={48} />
                    </div>
                    <h1 className="text-5xl font-black tracking-tighter text-white elite-gradient-text leading-tight mb-4">COMMAND_ACCESS</h1>
                    <p className="text-slate-500 font-bold text-sm uppercase tracking-[0.3em]">Institutional Execution Gateway</p>
                </div>

                {/* Login Card */}
                <div className="glass-card p-12 overflow-hidden relative">
                    <div className="flex items-center gap-3 mb-10 p-4 bg-primary bg-opacity-5 rounded-2xl border border-primary border-opacity-10">
                        <ShieldCheck className="text-primary" size={20} />
                        <span className="text-[10px] font-black text-primary uppercase tracking-[0.2em]">ENCRYPTED_SESSION_v4.2</span>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-8">
                        <div className="form-control space-y-3">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Identity_Protocol</label>
                            <div className="relative group">
                                <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors" size={20} />
                                <input
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary pl-12 h-16 rounded-2xl font-bold text-white placeholder:text-slate-700"
                                    placeholder="operator@nebu-trader.com"
                                />
                            </div>
                        </div>

                        <div className="form-control space-y-3">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1">Access_Key</label>
                            <div className="relative group">
                                <Key className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors" size={20} />
                                <input
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="input input-bordered w-full bg-neutral bg-opacity-30 border-white border-opacity-5 focus:border-primary pl-12 h-16 rounded-2xl font-bold text-white placeholder:text-slate-700"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className={`btn btn-primary w-full h-18 rounded-2xl text-xs font-black uppercase tracking-[0.3em] shadow-lg shadow-primary/20 transition-all duration-300 ${loading ? 'loading' : ''}`}
                        >
                            {loading ? 'VALIDATING...' : 'ESTABLISH_CONNECTION'}
                            {!loading && <ArrowRight size={20} className="ml-2" />}
                        </button>
                    </form>

                    <div className="mt-12 pt-8 border-t border-white border-opacity-5 text-center">
                        <p className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">
                            New Operator? <Link to="/register" className="text-primary hover:text-white transition-colors font-black underline underline-offset-8">PROVISION_NEW_ID</Link>
                        </p>
                    </div>
                </div>

                {/* Bottom Vitals */}
                <div className="mt-12 grid grid-cols-2 gap-6">
                    {[
                        { label: 'Latency', value: '04ms SYNC', icon: CheckCircle2, color: 'text-success' },
                        { label: 'Integrity', value: 'SHA-512 OK', icon: Lock, color: 'text-info' }
                    ].map((item, i) => (
                        <div key={i} className="flex flex-col items-center p-6 glass-card bg-opacity-10 border-opacity-5">
                            <item.icon size={20} className={`${item.color} mb-3`} />
                            <p className="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em] mb-1">{item.label}</p>
                            <p className="text-[11px] font-black text-white uppercase tracking-wider">{item.value}</p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Background Decoration */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary opacity-[0.03] rounded-full blur-[120px] pointer-events-none" />
        </div>
    );
};

export default Login;

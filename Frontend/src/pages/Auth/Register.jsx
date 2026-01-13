import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../../services/api';
import { Globe, UserPlus, Mail, Lock, ShieldCheck, CheckSquare, ArrowRight } from 'lucide-react';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await authService.register(formData);
            alert("Identity Provisioned. Proceed to Security Authentication.");
            navigate('/login');
        } catch (err) {
            alert("Operational Stop: Provisioning Logic Error");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#f8fafc] flex flex-col items-center justify-center p-6 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]">
            <div className="max-w-[500px] w-full animate-biz">
                <div className="flex flex-col items-center mb-10 text-center">
                    <div className="w-20 h-20 bg-blue-600 rounded-[28px] flex items-center justify-center mb-6 shadow-2xl shadow-blue-500/20 ring-4 ring-white">
                        <Globe className="text-white" size={32} />
                    </div>
                    <h1 className="text-4xl font-bold tracking-tight text-slate-900 font-heading leading-tight">Identity Provisioning</h1>
                    <p className="text-slate-500 font-medium mt-3 text-lg leading-relaxed truncate px-4">Establishing secure corporate access for Alpha-Network operators.</p>
                </div>

                <div className="biz-card p-12 bg-white/90 backdrop-blur-md shadow-2xl shadow-slate-200/60 border-slate-200/80">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Operator Alias / Handle</label>
                            <input
                                type="text"
                                required
                                value={formData.username}
                                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                className="w-full bg-slate-50 border border-slate-200 px-4 py-4 rounded-xl text-slate-900 outline-none focus:ring-4 focus:ring-blue-500/5 focus:border-blue-500/50 font-semibold text-[15px] transition-all"
                                placeholder="OP_7829_SEC"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Corporate Communications Address</label>
                            <input
                                type="email"
                                required
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                className="w-full bg-slate-50 border border-slate-200 px-4 py-4 rounded-xl text-slate-900 outline-none focus:ring-4 focus:ring-blue-500/5 focus:border-blue-500/50 font-semibold text-[15px] transition-all"
                                placeholder="operator.id@nebu-corp.global"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-[11px] font-bold text-slate-400 uppercase tracking-widest pl-1">Encryption Protocol / Password</label>
                            <input
                                type="password"
                                required
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                className="w-full bg-slate-50 border border-slate-200 px-4 py-4 rounded-xl text-slate-900 outline-none focus:ring-4 focus:ring-blue-500/5 focus:border-blue-500/50 font-semibold text-[15px] transition-all"
                                placeholder="••••••••"
                            />
                        </div>

                        <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 flex items-start gap-4">
                            <CheckSquare className="text-blue-600 mt-1 shrink-0" size={18} />
                            <p className="text-[11px] font-bold text-slate-500 leading-relaxed uppercase tracking-tight">I acknowledge and accept the corporate compliance regulations and terminal operation logs monitoring.</p>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full h-16 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-bold uppercase tracking-[0.2em] shadow-2xl shadow-blue-500/20 transition-all active:scale-[0.98] flex items-center justify-center gap-3 mt-4"
                        >
                            {loading ? 'Initializing Core...' : 'Initialize Identity'}
                            <ArrowRight size={20} className="mt-0.5" />
                        </button>
                    </form>

                    <div className="mt-12 pt-8 border-t border-slate-100/50 text-center">
                        <p className="text-[11px] font-bold text-slate-400 uppercase tracking-widest">
                            Already Provisioned? <Link to="/login" className="text-blue-600 hover:text-blue-700 font-extrabold underline underline-offset-4 tracking-[0.05em]">Secure Login</Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;

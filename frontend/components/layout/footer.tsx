import Link from "next/link";
import { Logo } from "@/components/ui/logo";
import { Facebook, Instagram, Twitter, Linkedin, MapPin, Phone, Mail } from "lucide-react";

export function Footer() {
    return (
        <footer className="bg-neutral-900 text-white pt-16 pb-8">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
                    {/* Brand Column */}
                    <div className="space-y-4">
                        <Logo variant="white" />
                        <p className="text-neutral-400 text-sm leading-relaxed max-w-xs">
                            Il servizio di riparazioni urgenti n.1 in Italia. Connettiamo professionisti qualificati con chi ha bisogno di assistenza immediata.
                        </p>
                        <div className="flex gap-4 pt-2">
                            <a href="#" className="text-neutral-400 hover:text-white transition-colors"><Facebook className="h-5 w-5" /></a>
                            <a href="#" className="text-neutral-400 hover:text-white transition-colors"><Instagram className="h-5 w-5" /></a>
                            <a href="#" className="text-neutral-400 hover:text-white transition-colors"><Twitter className="h-5 w-5" /></a>
                            <a href="#" className="text-neutral-400 hover:text-white transition-colors"><Linkedin className="h-5 w-5" /></a>
                        </div>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h3 className="text-lg font-bold mb-6 text-white">Servizi</h3>
                        <ul className="space-y-3 text-sm text-neutral-400">
                            <li><Link href="#" className="hover:text-primary transition-colors">Idraulico</Link></li>
                            <li><Link href="#" className="hover:text-primary transition-colors">Elettricista</Link></li>
                            <li><Link href="#" className="hover:text-primary transition-colors">Fabbro</Link></li>
                            <li><Link href="#" className="hover:text-primary transition-colors">Tuttofare</Link></li>
                            <li><Link href="#" className="hover:text-primary transition-colors">Caldaie & Clima</Link></li>
                        </ul>
                    </div>

                    {/* Company */}
                    <div>
                        <h3 className="text-lg font-bold mb-6 text-white">Azienda</h3>
                        <ul className="space-y-3 text-sm text-neutral-400">
                            <li><Link href="#" className="hover:text-primary transition-colors">Chi Siamo</Link></li>
                            <li><Link href="#" className="hover:text-primary transition-colors">Come Funziona</Link></li>
                            <li><Link href="#" className="hover:text-primary transition-colors">Diventa Tecnico</Link></li>
                            <li><Link href="#" className="hover:text-primary transition-colors">Prezzi</Link></li>
                            <li><Link href="#" className="hover:text-primary transition-colors">Contatti</Link></li>
                        </ul>
                    </div>

                    {/* Contact */}
                    <div>
                        <h3 className="text-lg font-bold mb-6 text-white">Contatti</h3>
                        <ul className="space-y-4 text-sm text-neutral-400">
                            <li className="flex items-start gap-3">
                                <MapPin className="h-5 w-5 text-primary shrink-0" />
                                <span>Via Roma 123,<br />00100 Roma (RM)</span>
                            </li>
                            <li className="flex items-center gap-3">
                                <Phone className="h-5 w-5 text-primary shrink-0" />
                                <span>+39 06 1234 5678</span>
                            </li>
                            <li className="flex items-center gap-3">
                                <Mail className="h-5 w-5 text-primary shrink-0" />
                                <span>info@prontocasa.it</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <div className="border-t border-neutral-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-neutral-500">
                    <p>© 2026 Pronto Casa S.r.l. Tutti i diritti riservati.</p>
                    <div className="flex gap-6">
                        <Link href="#" className="hover:text-white">Privacy Policy</Link>
                        <Link href="#" className="hover:text-white">Termini di Servizio</Link>
                        <Link href="#" className="hover:text-white">Cookie Policy</Link>
                    </div>
                </div>
            </div>
        </footer>
    );
}

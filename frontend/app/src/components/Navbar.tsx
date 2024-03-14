import React from "react";

import Link from "next/link";
import { Button } from "./ui/button";

interface NavbarItem {
    title: string,
    href: string
}

const NAVBAR_ITEMS: NavbarItem[] = [
    {title: "Acerca de", href: "/about"},
    {title: "Estadísticas", href: "/stats"},
    {title: "¿Qué hacer si mis datos han sido filtrados?", href: "/what-now"},
    {title: "¿Cómo funciona?", href: "/how-it-works"},
    {title: "¡Notifícame!", href: "/notifications"},
]

const Navbar = () => {
    return (
        <>
            <nav className="w-full relative top-0 z-40 ">
                <div className="container mx-auto">
                    <div className="flex items-center justify-between py-2">
                        <div className="flex w-1/4 items-center justify-between">
                            {/* Logo Sitio */}
                            <Link href="/" className="block">
                                <h1 className="text-lg font-bold">Data-Leak-Checker</h1>
                            </Link>
                        </div>
                        <div className="flex w-3/4 flex-wrap items-center justify-between">
                        {NAVBAR_ITEMS.map((item) => (
                            <Button key={item.title} variant="outline" asChild>
                                <Link href={item.href} className="block">
                                    <h3 className="font-bold">{item.title}</h3>
                                </Link>
                            </Button>
                        ))}
                        </div>
                        {/* <div className="flex">
                            <Link
                                href={process.env.NEXT_PUBLIC_BACKEND_URL + "/auth/login"}
                                className="bg-light-grey-fablab hover:bg-light-grey-fablab-dark text-grey-fablab flex items-center px-4 py-2 h-12 border-4 border-light-grey-fablab transition-colors duration-200"
                                title="Iniciar sesión"
                            >
                                INICIAR SESIÓN
                            </Link>
                            <button
                                type="button"
                                className="bg-grey-fablab hover:bg-grey-fablab-dark hover:cursor-pointer text-light-grey-fablab flex items-center px-4 py-2 h-12 border-4 border-light-grey-fablab transition-colors duration-200"
                                title="Hazte parte"
                            >
                                HAZTE PARTE
                            </button>
                        </div> */}
                    </div>
                </div>
            </nav >
        </>
    );
};

export default Navbar;
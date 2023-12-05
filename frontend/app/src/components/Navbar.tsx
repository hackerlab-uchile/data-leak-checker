import React from "react";
import Image from "next/image";
import { useState } from "react";

import Link from "next/link";
import { usePathname } from "next/navigation";

const BASE_IMAGE_URL = "https://cdn.discordapp.com/avatars/";
const DEFAULT_AVATAR = "/discord-icon.png";

const Navbar = () => {
    return (
        <>
            <nav className="text-white-fablab-text w-full relative top-0 z-40 ">
                <div className="container mx-auto">
                    <div className="flex items-center justify-between py-4">
                        <div className="flex items-center justify-between">
                            {/* Logo fablab */}
                            <Link href="/" className="block">
                                <h1 className="text-lg font-bold">Data-Leak-Checker</h1>
                            </Link>
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
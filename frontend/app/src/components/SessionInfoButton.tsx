import { useAuth } from "@/contexts/AuthContext";
import { Button } from "./ui/button";
import Link from "next/link";
import { useRouter } from "next/router";
import { RiArrowDropDownLine } from "react-icons/ri";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { FaCircleUser } from "react-icons/fa6";
import { useEffect, useState } from "react";
import { Separator } from "./ui/separator";
import { IoLogOutOutline } from "react-icons/io5";

export default function SessionInfoButton() {
  const { user, login, logout, ready } = useAuth();
  const router = useRouter();
  const [timeLeft, setTimeLeft] = useState<number>(0);

  function startTimer(dateString: string) {
    let timeDifference = new Date(dateString).getTime() - Date.now();
    setTimeLeft(timeDifference);
    const timer = setInterval(() => {
      setTimeLeft((time) => {
        if (time <= 1) {
          clearInterval(timer);
          return 0;
        } else {
          return time - 1000;
        }
      });
    }, 1000);
    return timer;
  }

  function timeLeftCustomFormatting(timestamp: number): string {
    let date = new Date(timestamp);
    let minutes = date.getUTCMinutes();
    let seconds = date.getUTCSeconds();
    return `${
      Math.floor(minutes / 10) > 0 ? minutes : "0" + minutes.toString()
    }:${Math.floor(seconds / 10) > 0 ? seconds : "0" + seconds.toString()}`;
  }

  useEffect(() => {
    // if (ready) {
    if (ready && user) {
      let timer = startTimer(user.exp);
      // let date = new Date();
      // date.setHours(date.getHours(), date.getMinutes() + 20, 15);
      // let timer = startTimer(date.toISOString());
      return () => clearInterval(timer);
    }
  }, [ready]);

  return (
    <div className="flex flex-1 flex-shrink-0 w-full">
      {user && timeLeft > 0 ? (
        <Button
          type="button"
          className="self-end justify-self-end"
          onClick={logout}
          variant="outline"
          asChild
        >
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">
                <p className="mr-1">{timeLeftCustomFormatting(timeLeft)}</p>
                <Separator orientation="vertical" />
                <FaCircleUser className="mx-1" size={"2em"} />
                <RiArrowDropDownLine size={"2em"} />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuLabel>{user.value}</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem asChild>
                <Link href={`/?search=${user.value}&type=${user.dtype}`}>
                  Ver filtraciones
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={(e) => logout()}>
                <IoLogOutOutline className="mx-1" size={"1.5em"} />
                Cerrar Sesión
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </Button>
      ) : (
        // <Button
        //   className="self-end justify-self-end"
        //   onClick={logout}
        //   variant="outline"
        //   asChild
        // >
        //   <Link href={"/"} className="block">
        //     <h3 className="font-bold">Cerrar Sesión</h3>
        //   </Link>
        // </Button>
        <Button className="self-end justify-self-end" variant="outline" asChild>
          <Link href={"/verification"} className="block">
            <h3 className="font-bold">Autenticarse</h3>
          </Link>
        </Button>
      )}
    </div>
  );
}

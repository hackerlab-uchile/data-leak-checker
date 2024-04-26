import Navbar from "@/components/Navbar";
import CryptoJS from "crypto-js";
import { FormEvent, Suspense, useEffect, useState } from "react";
import { Breach } from "@/models/Breach";
import { QueryType, getBreachesByQueryType } from "@/api/api";
import { PiShieldWarningFill } from "react-icons/pi";
import { MdError } from "react-icons/md";
import { FaCheckCircle } from "react-icons/fa";
import { IconContext } from "react-icons";
import { useRouter } from "next/router";
import Search from "@/components/Search";

const redColor = "#ED342F";

export default function Home() {
  const router = useRouter();
  const [newSearch, setNewSearch] = useState("");
  const searchedEmail = router.query.search ? String(router.query.search) : "";
  const [breaches, setBreaches] = useState<Array<Breach>>([]);
  const [responseReceived, setResponseReceived] = useState(false);

  async function get_breaches() {
    const emailQuery = CryptoJS.SHA256(searchedEmail).toString(
      CryptoJS.enc.Hex
    );
    console.log(emailQuery);
    const breachesList: Breach[] = await getBreachesByQueryType(
      emailQuery,
      QueryType.Email
    );
    console.log(breachesList);
    setBreaches(breachesList);
    setResponseReceived(true);
  }

  useEffect(() => {
    if (searchedEmail) {
      get_breaches();
    } else {
      router.push("/");
    }
    return () => {
      setBreaches([]);
    };
  }, [searchedEmail]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-24 pt-5">
      <Navbar />
      {/* <Search
        placeholder={"Consulte un email..."}
        searchTerm={newSearch}
        setSearchTerm={setNewSearch}
      /> */}
      <p className="self-center text-zinc-400">Correo consultado:</p>
      <h2 className="text-2xl font-bold self-center">{searchedEmail}</h2>
      {responseReceived ? (
        <div className="flex flex-col mt-5 w-full items-center justify-start">
          <div className="flex flex-col w-full self-start justifiy-start items-center">
            {breaches.length > 0 ? (
              <IconContext.Provider value={{ color: `${redColor}` }}>
                <PiShieldWarningFill fontSize="3.5em" className="self-center" />
                <AlertMessage
                  boxColor="bg-red-hackerlab"
                  message={`¡Este correo ha sido visto en ${breaches.length} filtraciones de nuestro conocimiento!`}
                />
              </IconContext.Provider>
            ) : (
              <IconContext.Provider value={{ color: "green" }}>
                <FaCheckCircle
                  color="green"
                  fontSize="3.5em"
                  className="self-center"
                />
                <AlertMessage
                  boxColor="bg-green-hackerlab"
                  message="¡Este correo no ha sido encontrado en filtraciones de nuestro conocimiento!"
                />
              </IconContext.Provider>
            )}
          </div>
          {breaches.map((breach) => (
            <BreachCard key={breach.id} breach={breach} />
          ))}
        </div>
      ) : (
        <Suspense fallback={<p>Buscando...</p>}></Suspense>
      )}

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}

function BreachCard({ breach }: { breach: Breach }) {
  return (
    <div className="flex flex-col items-start my-1 p-4 border rounded-lg w-full">
      <h4 className="font-bold text-lg">
        {`${breach.name} (${breach.breach_date.slice(0, 4)})`}
      </h4>
      <p>{breach.description}</p>
      <p>
        <b>Datos comprometidos</b>
      </p>
      <div className="flex flex-col">
        <div className="flex flex-row items-center">
          <p>Contraseña</p>
          <MdError color="red"></MdError>
        </div>
        <div className="flex flex-row items-center">
          <p>Contraseña</p>
          <MdError style={{ fill: `${redColor}` }}></MdError>
        </div>
      </div>
    </div>
  );
}

function AlertMessage({
  message,
  boxColor,
}: {
  message: string;
  boxColor: string;
}) {
  return (
    <div
      className={`flex px-3 rounded-md justify-center text-white ${boxColor} w-[90%]`}
    >
      <p className="text-xl text-center">{message}</p>
    </div>
  );
}

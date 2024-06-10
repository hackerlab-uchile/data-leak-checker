import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import Search from "@/components/Search";
import Navbar from "@/components/Navbar";
import { FormEvent, useEffect, useState } from "react";
import { DataLeak } from "@/models/Breach";
import { getDataLeaksByValueAndType, QueryType } from "@/api/api";
import { FaCheckCircle } from "react-icons/fa";
import { MdOutlineSecurity } from "react-icons/md";
import { FaIdCard } from "react-icons/fa";
import { MdOutlinePhishing } from "react-icons/md";
import { FcIdea } from "react-icons/fc";
import { FaUnlock } from "react-icons/fa6";
import { AiOutlineSafety } from "react-icons/ai";
import { useRouter } from "next/router";
import { IconContext } from "react-icons";
import { PiShieldWarningFill } from "react-icons/pi";
import { LeaksTable } from "@/components/breaches/leaks-table";
import { ColumnDef } from "@tanstack/react-table";
import {
  TypesLeak,
  getLeakTableColumns,
  getLeakTableRows,
} from "@/components/breaches/columns";
import { LuMailWarning } from "react-icons/lu";
import { Loader2 } from "lucide-react";
import BreachCard from "@/components/BreachCard";
import AlertMessage from "@/components/AlertMessage";
import { safetyTips } from "@/utils/webSafetyTips";

const redColor = "#ED342F";

export default function Home() {
  const router = useRouter();
  const [searchEmail, setSearchEmail] = useState("");
  const [responseReceived, setResponseReceived] = useState(false);
  const [error, setError] = useState<boolean>(false);
  const [waitingResponse, setWaitingResponse] = useState(false);
  const [searchRut, setSearchRut] = useState("");
  const [searchPhone, setSearchPhone] = useState("");
  const [dataLeaks, setDataLeaks] = useState<Array<DataLeak>>([]);
  const [columns, setColumns] = useState<ColumnDef<TypesLeak>[]>([]);
  const [tableData, setTableData] = useState<TypesLeak[]>([]);

  async function handleEmailSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const emailQuery = searchEmail.trim().toLowerCase();
    if (emailQuery) {
      setResponseReceived(false);
      setWaitingResponse(true);
      const [dataLeaksList, gotError]: [DataLeak[], boolean] =
        await getDataLeaksByValueAndType(emailQuery, QueryType.Email);
      setError(gotError);
      setDataLeaks(dataLeaksList);
      setResponseReceived(true);
      setWaitingResponse(false);
    }
  }

  async function handleRutSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const rutQuery = searchRut
      .trim()
      .replace(/\s/g, "")
      .replace(/\./g, "")
      .replace("-", "");
    if (rutQuery) {
      setResponseReceived(false);
      setWaitingResponse(true);
      console.log("Query:", rutQuery);
      const [dataLeaksList, gotError]: [DataLeak[], boolean] =
        await getDataLeaksByValueAndType(rutQuery, QueryType.Rut);
      setError(gotError);
      setDataLeaks(dataLeaksList);
      setResponseReceived(true);
      setWaitingResponse(false);
    } else {
      console.log("Not valid rut!");
    }
  }

  async function handlePhoneSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const phoneQuery = searchPhone.trim();
    if (phoneQuery) {
      setResponseReceived(false);
      setWaitingResponse(true);
      const [dataLeaksList, gotError]: [DataLeak[], boolean] =
        await getDataLeaksByValueAndType(phoneQuery, QueryType.Phone);
      setError(gotError);
      setDataLeaks(dataLeaksList);
      setResponseReceived(true);
      setWaitingResponse(false);
    }
  }

  useEffect(() => {
    if (dataLeaks.length > 0) {
      setColumns(getLeakTableColumns(dataLeaks));
      setTableData(getLeakTableRows(dataLeaks));
    }
  }, [dataLeaks]);

  const searchKeys = [
    {
      title: "Email",
      value: "email",
      description:
        "Ingrese el correo electrónico que desea consultar. Se revisará si dicho correo fue encontrado en alguna filtración de datos que tengamos conocimiento.",
      submitFunc: handleEmailSearch,
      search: searchEmail,
      setSearch: setSearchEmail,
      inputHint: "Consulte un email...",
      name: "correo",
    },
    {
      title: "RUT",
      value: "rut",
      description:
        "Ingrese el RUT que desea consultar. Se revisará si dicho RUT fue encontrado en alguna filtración de datos que tengamos conocimiento.",
      submitFunc: handleRutSearch,
      search: searchRut,
      setSearch: setSearchRut,
      inputHint: "Consulte un RUT...",
      name: "RUT",
    },
    {
      title: "Número telefónico",
      value: "phone",
      description:
        "Ingrese el número telefónico que desea consultar. Se revisará si dicho número fue encontrado en alguna filtración de datos que tengamos conocimiento." +
        "\nRecuerde que un número celular tiene el siguiente formato 9 XXXX XXXX, mientras que uno particular 22 XXXX XXX.",
      submitFunc: handlePhoneSearch,
      search: searchPhone,
      setSearch: setSearchPhone,
      inputHint: "Consulte un número telefónico...",
      name: "número telefónico",
    },
  ];

  function clearSearchIput() {
    setSearchEmail("");
    setSearchPhone("");
    setSearchRut("");
    setResponseReceived(false);
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-start md:px-24 pt-2 pb-20">
      <Navbar />
      <div className="flex flex-col mt-5 w-full items-center justify-start">
        {/* </div> */}

        {/* <div className="z-10 max-w-5xl w-full font-mono text-sm lg:flex flex-col"> */}
        {/* <div className='flex-col w-[80%]'> */}
        <div className="flex flex-col w-full items-center text-center py-3">
          <h2 className="font-black text-2xl text-cyan-500">
            ¡Bienvenid@ a Data Leak Checker!
          </h2>
          <p className="text-lg w-[90%]">
            ¡En esta plataforma podrás enterarte qué datos privados tuyos han
            sido encontrados en filtraciones de datos!
          </p>
        </div>
        <POCMessage></POCMessage>
        {/* <h3 className="font-bold">Consultar por:</h3> */}
        <Tabs
          defaultValue="email"
          className="w-[90%] md:w-[80%] max-w-[1280px]"
        >
          <TabsList className="grid w-full grid-cols-3">
            {searchKeys.map((item) => (
              <TabsTrigger
                onClick={clearSearchIput}
                key={item.value}
                value={item.value}
              >
                {item.title}
              </TabsTrigger>
            ))}
          </TabsList>
          {searchKeys.map((item) => (
            <TabsContent key={item.value} value={item.value}>
              <Card>
                <CardHeader>
                  <CardTitle>{item.title}</CardTitle>
                  <CardDescription>{item.description}</CardDescription>
                </CardHeader>
                <form
                  onSubmit={item.submitFunc}
                  autoComplete="off"
                  className="w-full"
                >
                  <CardContent className="space-y-2">
                    <div className="z-10 max-w-5xl w-full items-center self-center justify-self-center justify-between font-mono text-sm lg:flex">
                      <Search
                        placeholder={item.inputHint}
                        searchTerm={item.search}
                        setSearchTerm={item.setSearch}
                      />
                    </div>
                  </CardContent>
                  <CardFooter className="flex flex-row items-center justify-center">
                    {/* <Link
                      href={{
                        pathname: "/search",
                        query: { search: `${searchEmail}` },
                      }}
                    > */}
                    <Button type="submit">Buscar</Button>
                    {/* </Link> */}
                  </CardFooter>
                </form>
              </Card>
              {responseReceived ? (
                <>
                  {!error ? (
                    <div className="flex flex-col mt-5 w-full items-center justify-start">
                      <div className="flex flex-col w-full self-start justifiy-start items-center">
                        {dataLeaks.length > 0 ? (
                          <>
                            <IconContext.Provider
                              value={{ color: `${redColor}` }}
                            >
                              <PiShieldWarningFill
                                fontSize="3.5em"
                                className="self-center"
                              />
                              <AlertMessage
                                variant="danger"
                                message={`¡Este ${item.name} ha sido visto en ${dataLeaks.length} filtraciones de nuestro conocimiento!`}
                              />
                            </IconContext.Provider>
                            {/* <div className="container mx-auto py-10"> */}
                            <div className="w-full mx-auto py-5">
                              <LeaksTable
                                columns={columns}
                                data={tableData}
                                queried_type={item.name}
                              />
                            </div>
                          </>
                        ) : (
                          <>
                            <FaCheckCircle
                              // color="green"
                              fontSize="3.5em"
                              className="self-center text-green-hackerlab"
                            />
                            <AlertMessage
                              variant="safe"
                              message={`¡Este ${item.name} no ha sido encontrado en filtraciones de nuestro conocimiento!`}
                            />
                            <div className="p-3 my-5 flex flex-col justify-center w-full sm:w-[90%] border rounded-md border-cyan-400">
                              <h3 className="flex flex-row text-lg font-bold underline">
                                <FcIdea className="mt-1"></FcIdea>
                                Recomendaciones de seguridad
                              </h3>
                              {safetyTips.map((tip, index) => (
                                <div
                                  className="ml-3 items-start flex flex-row gap-1 text-lg"
                                  key={index}
                                >
                                  <AiOutlineSafety
                                    className="mt-1.5 shrink-0"
                                    color="green"
                                  ></AiOutlineSafety>
                                  <p className="font-thin m-0">
                                    <b>{tip.title}: </b>
                                    {tip.value}
                                  </p>
                                </div>
                              ))}
                              <p></p>
                            </div>
                          </>
                        )}
                      </div>
                      {dataLeaks.map((dLeak, index) => (
                        <BreachCard
                          key={index}
                          breach={dLeak.breach}
                          index={index}
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="my-5 w-full text-center">
                      <p className="text-lg text-red-hackerlab">
                        Error: por favor, inténtelo de nuevo más tarde
                      </p>
                    </div>
                  )}
                </>
              ) : (
                <>
                  {waitingResponse ? (
                    <div className="mt-10 flex w-full justify-center">
                      <Loader2 size={"3em"} className="animate-spin"></Loader2>
                    </div>
                  ) : (
                    // <p>Buscando...</p>
                    // Landing page
                    <LandingPage></LandingPage>
                  )}
                </>
              )}
            </TabsContent>
          ))}
        </Tabs>
        {/* </div> */}
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}

function POCMessage({}) {
  return (
    <div className="w-[90%] md:w-[80%] max-w-[1280px] rounded-md border-2 px-3 mb-4 border-red-600 bg-red-300">
      <p className="font-bold">Leer antes de usar:</p>
      <p>
        Los datos de filtraciones presentes son <b>100% falsos</b>. Los datos
        entregados son totalmente al azar, y no corresponden a ninguna
        filtración de datos del mundo real. Este sitio es solamente una prueba
        de concepto con el fin de averiguar si la información presentada es
        comprensible para un futuro usuario.
      </p>
    </div>
  );
}

const LandingPage = ({}) => {
  return (
    <div className="flex flex-col divide-y pt-7 text-center justify-center w-full">
      <div className="py-3">
        <h2 className="font-bold text-xl">¿Qué es una filtración de datos?</h2>
        <p className="italic text-muted-foreground">
          &ldquo;Una filtración de datos corresponde a cualquier incidente de
          seguridad en que{" "}
          <b>
            terceros no autorizadas ganan acceso a datos sensibles o información
            confidencial
          </b>
          &rdquo;
          {/* . Algunos ejemplos pueden ser datos personales (direcciones de
          correos, cuentas bancarias, contraseñas, RUTs) o datos corporativos
          (información de clientes, propiedad intelectual, información
          financiera).&rdquo; */}
        </p>
      </div>
      <div className="py-3">
        <h2 className="font-bold text-xl">
          ¿De qué me sirve esta información?
        </h2>
        <p className="text-muted-foreground">
          Es sumamente importante mantenerse informado y consciente de qué datos
          personales han caído en manos de terceros no autorizados. Agentes
          malintencionados pueden hacer uso de esta información para
          <b> obtener acceso a tus cuentas</b>, <b>suplantar tu identidad</b> e{" "}
          <b>incluso crear estafas más convincentes</b>.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 text-center py-5 justify-items-center">
          <div className="flex flex-col items-center">
            <FaUnlock fontSize={"5em"} className="my-3"></FaUnlock>
            <p className="text-muted-foreground">
              <b>Prevenir accesos a tus cuentas</b> por terceros, cambiando tu
              contraseñas/credenciales filtradas oportunamente
            </p>
            {/* <p className="text-muted-foreground">
              Obtener acceso a tus cuentas, mediantes contraseñas/credenciales
              filtradas
            </p> */}
          </div>
          <div className="flex flex-col items-center">
            <FaIdCard fontSize={"5em"} className="my-3"></FaIdCard>
            <p className="text-muted-foreground">
              <b>Evitar una suplantación de identidad</b>, conociendo qué datos
              peronales o credenciales se han visto comprometidas
            </p>
            {/* <p className="text-muted-foreground">
              Suplantación de identidad, al tener a disposición credenciales e
              información personal{" "}
            </p> */}
          </div>
          <div className="flex flex-col items-center">
            <LuMailWarning fontSize={"5em"} className="my-3"></LuMailWarning>
            {/* <MdOutlinePhishing
              fontSize={"5em"}
              className="my-3"
            ></MdOutlinePhishing> */}
            <p className="text-muted-foreground">
              <b>Estar atento/a frente a intentos de estafas</b>, relacionadas a
              la información filtrada
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

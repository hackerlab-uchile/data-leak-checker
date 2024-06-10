import Navbar from "@/components/Navbar";
import { Dispatch, SetStateAction, useEffect, useState } from "react";
import { DataLeak } from "@/models/Breach";
import { ColumnDef } from "@tanstack/react-table";
import {
  TypesLeak,
  getLeakTableColumns,
  getLeakTableRows,
} from "@/components/breaches/columns";
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
import {
  QueryType,
  sendVerificationEmail,
  sendVerificationSMS,
  verifyCode,
} from "@/api/api";
import { Loader2 } from "lucide-react";
import CircleNumber from "@/components/CircleNumber";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
} from "@/components/ui/input-otp";

import { GrPowerReset } from "react-icons/gr";
import { useRouter } from "next/navigation";
import { useToast } from "@/components/ui/use-toast";
import { Toaster } from "@/components/ui/toaster";

export default function VerificationHome() {
  const [step, setStep] = useState<number>(0);
  const [search, setSearch] = useState("");
  const [searchType, setSearchType] = useState<QueryType>(QueryType.Email);
  const [dataLeaks, setDataLeaks] = useState<Array<DataLeak>>([]);
  const [columns, setColumns] = useState<ColumnDef<TypesLeak>[]>([]);
  const [tableData, setTableData] = useState<TypesLeak[]>([]);

  useEffect(() => {
    if (dataLeaks.length > 0) {
      setColumns(getLeakTableColumns(dataLeaks));
      setTableData(getLeakTableRows(dataLeaks));
    }
  }, [dataLeaks]);

  let content: JSX.Element = <></>;
  if (step == 0) {
    content = (
      <PresentationContent step={step} setStep={setStep}></PresentationContent>
    );
  } else if (step == 1) {
    content = (
      <SearchContent
        step={step}
        setStep={setStep}
        search={search}
        setSearch={setSearch}
        setType={setSearchType}
      ></SearchContent>
    );
  } else if (step == 2) {
    content = (
      <CodeVerification
        step={step}
        setStep={setStep}
        search={search}
        setSearch={setSearch}
        searchType={searchType}
      ></CodeVerification>
    );
  } else {
    setStep(0);
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-start md:px-24 pt-2 pb-20">
      <Navbar />
      <div className="flex flex-col mt-20 w-full items-center justify-start">
        <div className="flex flex-row mb-3 self-start w-full items-center gap-x-5">
          <h2 className="text-xl font-bold">Filtraciones Sensibles</h2>
          <CircleNumber
            aNumber={step + 1}
            className="bg-primary text-primary-foreground"
          ></CircleNumber>
        </div>
        {content}
        <div className="w-[95%]">
          <Toaster />
        </div>
        <div className="flex flex-col">
          <div className="ml-3 flex flex-row items-start gap-1"></div>
        </div>
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}

const PresentationContent = ({
  step,
  setStep,
}: {
  step: number;
  setStep: Dispatch<SetStateAction<number>>;
}) => {
  return (
    <Card className="max-w-md">
      <CardHeader>
        <CardTitle>Filtraciones Sensibles</CardTitle>
        <CardDescription>¿Qué es una filtración sensible?</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-justify">
          Una filtración sensible es aquella que con tal solo se sepa qué datos
          estuvieron registrados (correo, RUT, teléfono, etc) en cierto
          servicio, pone en riesgo la reputación de los usuarios involucrados, o
          que lleve a otras consecuencias que los pudiese impactar
          negativamente.
        </p>
      </CardContent>
      <CardFooter>
        <Button
          type="button"
          onClick={(e) => {
            setStep(step + 1);
          }}
        >
          Empezar
        </Button>
      </CardFooter>
    </Card>
  );
};

const SearchContent = ({
  step,
  setStep,
  search,
  setSearch,
  setType,
}: {
  step: number;
  setStep: Dispatch<SetStateAction<number>>;
  search: string;
  setSearch: Dispatch<SetStateAction<string>>;
  setType: Dispatch<SetStateAction<QueryType>>;
}) => {
  const [inputError, setInputError] = useState("");
  const [waitingResponse, setWaitingResponse] = useState(false);

  async function handleEmailSubmit() {
    // TODO: Validate Email Format
    if (!search || waitingResponse) {
      return;
    }
    setWaitingResponse(true);
    setType(QueryType.Email);
    let errorMsg: string = await sendVerificationEmail(search);
    setWaitingResponse(false);
    if (errorMsg !== "") {
      setInputError(errorMsg);
    } else {
      setStep(step + 1);
    }
  }

  async function handlePhoneSubmit() {
    // TODO: Validate Phone Format
    if (!search || waitingResponse) {
      return;
    }
    setWaitingResponse(true);
    setType(QueryType.Phone);
    let errorMsg: string = await sendVerificationSMS(search);
    setWaitingResponse(false);
    if (errorMsg !== "") {
      setInputError(errorMsg);
    } else {
      setStep(step + 1);
    }
  }
  const searchKeys = [
    {
      title: "Email",
      value: "email",
      description:
        "Ingrese el correo electrónico que desea consultar. Se le enviará un código de 6-dígitos a su correo electrónico.",
      submitFunc: handleEmailSubmit,
      search: search,
      setSearch: setSearch,
      inputHint: "Ingrese un email...",
      name: "correo",
    },
    {
      title: "Número celular",
      value: "phone",
      description:
        "Ingrese el número celular que desea consultar. Se le enviará un código de 6-dígitos a su al celular ingresado mediante SMS." +
        "\nRecuerde que un número celular tiene el siguiente formato +56 9 XXXX XXXX, 56 9 XXXX XXXX o 9 XXXX XXXX.",
      submitFunc: handlePhoneSubmit,
      search: search,
      setSearch: setSearch,
      inputHint: "Ingrese un número celular...",
      name: "número telefónico",
    },
  ];
  return (
    // <Tabs defaultValue="email" className="w-[90%] md:w-[80%] max-w-[1280px]">
    <Tabs defaultValue="email" className="w-[90%] md:w-[80%] max-w-lg">
      <TabsList className="grid w-full grid-cols-2">
        {searchKeys.map((item) => (
          <TabsTrigger
            onClick={(e) => {
              setSearch("");
              setInputError("");
            }}
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
              onSubmit={(e) => {
                e.preventDefault();
                item.submitFunc();
              }}
              autoComplete="off"
              className="w-full"
            >
              <CardContent className="space-y-2">
                <div className="flex flex-col z-10 max-w-5xl w-full items-center self-center justify-self-center justify-between font-mono text-sm lg:flex">
                  <Search
                    placeholder={item.inputHint}
                    searchTerm={item.search}
                    setSearchTerm={item.setSearch}
                  />
                  {inputError !== "" && (
                    <p className="text-red-hackerlab text-center">
                      {inputError}
                    </p>
                  )}
                </div>
              </CardContent>
              <CardFooter className="flex flex-row items-center justify-center">
                {waitingResponse == false ? (
                  <Button type="submit">Buscar</Button>
                ) : (
                  <Button variant={"outline"} disabled={true}>
                    <Loader2 size={"2em"} className="animate-spin"></Loader2>
                  </Button>
                )}
              </CardFooter>
            </form>
          </Card>
        </TabsContent>
      ))}
    </Tabs>
  );
};

const CodeVerification = ({
  step,
  setStep,
  search,
  setSearch,
  searchType,
}: {
  step: number;
  setStep: Dispatch<SetStateAction<number>>;
  search: string;
  setSearch: Dispatch<SetStateAction<string>>;
  searchType: QueryType;
}) => {
  const COOLDOWN_WAIT: number = 30;
  const [verificationCode, setVerificationCode] = useState<string>("");
  const [inputError, setInputError] = useState("");
  const [waitingResponse, setWaitingResponse] = useState(false);
  const [loadingNextPage, setLoadingNextPage] = useState(false);
  const [timeLeft, setTimeLeft] = useState(COOLDOWN_WAIT);
  const [startCooldown, setStartCooldown] = useState(true);
  const { push } = useRouter();
  const { toast } = useToast();

  async function handleResendCode() {
    if (timeLeft > 0) return;
    if (!search || waitingResponse) {
      toast({
        title: "Ha ocurrido un error. Por favor, refresque la página",
        variant: "destructive",
      });
      return;
    }
    setVerificationCode(""); // Empty code input
    setStartCooldown(true); // Start cooldown to wait before resending again
    setWaitingResponse(true);
    let errorMsg: string = await sendVerificationEmail(search);
    setWaitingResponse(false);
    if (errorMsg !== "") {
      toast({
        title: errorMsg,
        variant: "destructive",
      });
    } else {
      toast({
        title: "!Un nuevo código ha sido enviado con éxito!",
        variant: "successful",
      });
    }
  }

  async function handleCodeSubmit() {
    if (verificationCode.length == 6) {
      setWaitingResponse(true);
      let [isValid, errorMsg] = await verifyCode(
        verificationCode,
        search,
        searchType
      );
      if (isValid && errorMsg === "") {
        setInputError("");
        setLoadingNextPage(true);
        push("/sensitive");
      } else if (!isValid && errorMsg === "") {
        setInputError("Código incorrecto");
      } else {
        setInputError(errorMsg);
      }
      setWaitingResponse(false);
    }
  }

  function startTimer() {
    setStartCooldown(false);
    setTimeLeft(COOLDOWN_WAIT);
    let timer = setInterval(() => {
      setTimeLeft((time) => {
        if (time === 1) {
          clearInterval(timer);
          return 0;
        } else return time - 1;
      });
    }, 1000);
  }

  useEffect(() => {
    if (startCooldown) {
      startTimer();
    }
  }, [startCooldown]);

  useEffect(() => {
    if (inputError && verificationCode.length < 6) {
      setInputError("");
    }
  }, [inputError, verificationCode]);

  return (
    <Card className="max-w-lg">
      <CardHeader>
        <CardTitle>Ingresa el código de verificación enviado</CardTitle>
        <CardDescription>Código de 6-dígitos</CardDescription>
      </CardHeader>
      <CardContent>
        <p>
          Revise el buzón de entrada (o spam) de su correo electrónico, donde se
          le ha enviado un código de verificación de 6 dígitos.
        </p>
        <div className="flex flex-col mt-5 gap-y-5 items-center justify-center w-full">
          <InputOTP
            value={verificationCode}
            onChange={(value) => setVerificationCode(value)}
            maxLength={6}
            disabled={loadingNextPage ? true : false}
          >
            <InputOTPGroup>
              {Array.from(Array(3).keys()).map((i) => [
                <InputOTPSlot
                  key={i}
                  index={i}
                  className={
                    inputError.length === 0 ? "" : "border-red-hackerlab"
                  }
                />,
              ])}
            </InputOTPGroup>
            <InputOTPGroup>
              {Array.from(Array(3).keys()).map((i) => [
                <InputOTPSlot
                  key={i}
                  index={i + 3}
                  className={
                    inputError.length === 0 ? "" : "border-red-hackerlab"
                  }
                />,
              ])}
            </InputOTPGroup>
          </InputOTP>
          {inputError !== "" && (
            <p className="text-red-hackerlab text-center">{inputError}</p>
          )}
          <div className="flex flex-col items-center justify-center gap-y-1">
            <p className="text-sm text-muted-foreground">
              En caso de no aparecer, puede enviar un nuevo código
            </p>
            <Button
              type="button"
              variant={"secondary"}
              size="sm"
              onClick={(e) => {
                e.preventDefault();
                handleResendCode();
              }}
              disabled={loadingNextPage || timeLeft > 0 ? true : false}
            >
              {timeLeft <= 0 ? (
                <div className="flex flex-row gap-x-1 items-center">
                  <>Enviar nuevo código</>
                  <GrPowerReset />
                </div>
              ) : (
                <>Puede enviar nuevo código en {`${timeLeft}s`}</>
              )}
            </Button>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex flex-row justify-between">
        {waitingResponse || loadingNextPage ? (
          <Button variant={"outline"} className="w-full" disabled={true}>
            <Loader2 size={"2em"} className="animate-spin"></Loader2>
          </Button>
        ) : (
          <Button
            type="button"
            className="w-full"
            disabled={verificationCode.length !== 6 ? true : false}
            onClick={(e) => {
              e.preventDefault();
              handleCodeSubmit();
            }}
          >
            Verificar
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};
import { DataLeak } from "@/models/Breach";
import { ColumnDef } from "@tanstack/react-table";
import Link from "next/link";
import { MdError } from "react-icons/md";
import { TbShieldExclamation } from "react-icons/tb";
import { BsExclamationLg } from "react-icons/bs";
import { LuSearchX, LuShieldAlert, LuShieldQuestion } from "react-icons/lu";

export type TypesLeak = {
  filtración: string;
  [key: string]: string;
};

function getDataFoundList(dataLeaks: DataLeak[]): string[] {
  let dataFound: string[] = dataLeaks.reduce(
    (result: string[], current: DataLeak) =>
      // [...result].concat(current.found_with),
      [...result].concat(current.breach.breached_data),
    []
  );
  return dataFound.filter(function (elem, index, self) {
    return index === self.indexOf(elem);
  });
}

export function getLeakTableColumns(
  dataLeaks: DataLeak[]
): ColumnDef<TypesLeak>[] {
  const dataFoundUnique: string[] = [
    "filtración",
    ...getDataFoundList(dataLeaks),
  ];
  return dataFoundUnique.map((value) => {
    return {
      accessorKey: value,
      header: value.charAt(0).toUpperCase() + value.slice(1),
      cell: ({ row }) => {
        const index = row.index;
        const rowValue = row.getValue(value);
        if (rowValue == "no") {
          return (
            <div className="flex justify-center text-center w-full">
              {/* <>No visto</> */}
              <LuSearchX fontSize="2.0em" color="gray"></LuSearchX>
              {/* <LuShieldQuestion
                fontSize="2.0em"
                color="gray"
              ></LuShieldQuestion> */}
            </div>
          );
        } else if (rowValue == "yes") {
          return (
            <div className="flex justify-center text-center w-full">
              {/* <LuShieldAlert
                fontSize="2em"
                color="red"
                className="text-center"
              ></LuShieldAlert> */}
              <TbShieldExclamation
                fontSize="2em"
                color="red"
                className="text-center"
              ></TbShieldExclamation>
              {/* <BsExclamationLg fontSize="3em" color="red"></BsExclamationLg> */}
            </div>
          );
        } else if (rowValue == "-") {
          return (
            <div className="flex justify-center text-center w-full">-</div>
          );
        } else {
          return typeof rowValue == "string" ? (
            <a href={`#${index}`}>
              <strong>{rowValue}</strong>
            </a>
          ) : (
            ""
          );
        }
      },
    };
  });
}

export function getLeakTableRows(dataLeaks: DataLeak[]): TypesLeak[] {
  const rawColumns: string[] = getDataFoundList(dataLeaks);
  return dataLeaks.map((dl: DataLeak) => {
    let data: TypesLeak = {
      filtración: `${dl.breach.name} (${dl.breach.breach_date.slice(0, 4)})`,
    };
    rawColumns.forEach((col) => {
      if ([dl.data_type, ...dl.found_with].includes(col)) {
        data[col] = "yes";
      } else if (dl.breach.breached_data.includes(col)) {
        data[col] = "no";
      } else {
        data[col] = "-";
      }
      // data[col] = [dl.data_type, ...dl.found_with].includes(col) ? "yes" : "no";
    });
    return data;
  });
}

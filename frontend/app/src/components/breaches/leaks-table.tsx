import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { LuSearchX } from "react-icons/lu";
import { TbShieldExclamation } from "react-icons/tb";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  queried_type: string;
}

export function LeaksTable<TData, TValue>({
  columns,
  data,
  queried_type,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div>
      <h2 className="text-center font-bold">DATOS COMPROMETIDOS</h2>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead className="text-center" key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell
                      // className={cn("border", "[&_td:last-child]:border-0")}
                      // className="border"
                      key={cell.id}
                    >
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="py-3 grid grid-cols-2 sm:grid-cols-4 gap-y-1 justify-items-center">
        <p className="text-sm flex flex-row items-center">
          <TbShieldExclamation
            fontSize="1.5em"
            color="red"
            className="shrink-0 text-center"
          ></TbShieldExclamation>
          : Encontrado en la filtración
        </p>
        <p className="text-sm flex flex-row items-center">
          - : Dato no filtrado
        </p>
        <div className="col-span-2 text-sm flex flex-row items-center">
          <p className="flex flex-row">
            <LuSearchX
              className="shrink-0"
              fontSize="1.5em"
              color="gray"
            ></LuSearchX>
            :
          </p>
          <p className="ml-2">
            No visto junto al {queried_type.toLowerCase()} consultado. Sin
            embargo, esto puede significar que no lo hayamos visto, pero
            igualmente se haya visto filtrado.
            {/* No visto junto al {queried_type.toLowerCase()} consultado. Sin
            embargo, esto no quiere decir que haya no haya sido filtrado. */}
          </p>
        </div>
      </div>
    </div>
  );
}

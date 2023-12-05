
import { Dispatch, SetStateAction } from "react";
import { FaSearch } from "react-icons/fa";

// import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function Search({ placeholder, searchTerm, setSearchTerm }: { placeholder: string, searchTerm: string, setSearchTerm: Dispatch<SetStateAction<string>> }) {
    function handleSearch(term: string) {
        setSearchTerm(term);
    }

    return (
        <div className="relative flex flex-1 flex-shrink-0 w-full">
            <label htmlFor="search" className="sr-only">
                Search
            </label>
            <input
                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                placeholder={placeholder}
                name={"search"}
                onChange={(e) => {
                    handleSearch(e.target.value);
                }}
            />
            <FaSearch className="absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
        </div>
    );
}
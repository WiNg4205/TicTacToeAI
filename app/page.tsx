"use client"

import { useEffect, useState } from "react";
import Image from "next/image";

export default function Home() {
  const [win, setWin] = useState<string | null>(null);
  const [grid, setGrid] = useState([
      [" ", " ", " "],
      [" ", " ", " "],
      [" ", " ", " "]
    ]);

  const winList = [
    [[0,0], [0,1], [0,2]],
    [[1,0], [1,1], [1,2]],
    [[2,0], [2,1], [2,2]],
    [[0,0], [1,0], [2,0]],
    [[0,1], [1,1], [2,1]],
    [[0,2], [1,2], [2,2]],
    [[0,0], [1,1], [2,2]],
    [[2,0], [1,1], [0,2]],
  ];

  const restart = () => {
    setGrid([
      [" ", " ", " "],
      [" ", " ", " "],
      [" ", " ", " "]
    ]);
    setWin(null);
  }

  const placeSquare = async (row: number, col: number) => {
    if (win || grid[row][col] !== " ") return;
  
    const newGrid = grid.map((rowArr, i) => 
      rowArr.map((cell, j) => (i === row && j === col ? "O" : cell))
    );
  
    setGrid(newGrid);
    if (checkWin(newGrid)) return;
    
    const response = await fetch(process.env.NEXT_PUBLIC_API as string, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ grid: newGrid })
    });
  
    const data = await response.json();
    setGrid(data["new_grid"]);
  }

  const checkWin = (grid: string[][]) => {
    for (const winCondition of winList) {
      if (winCondition.every(([x, y]) => grid[x][y] === "O")) {
        setWin("O");
        return true;
      }
    }
    return false;
  }

  const checkLose = () => {
    for (const winCondition of winList) {
      if (winCondition.every(([x, y]) => grid[x][y] === "X")) {
        setWin("X");
      }
    }
  }

  useEffect(() => {
    if (grid) {
      checkLose();
    }
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === 'r' || event.key === 'R') {
        restart();
      }
    };

    window.addEventListener('keydown', handleKeyPress);

    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [grid]);

  return (
    <div className="flex flex-col items-center">
      <div className="h-8 w-1/2 relative">
        {win === "O" && <div className="font-bold text-2xl">You Win!</div>}
        {win === "X" && <div className="font-bold text-2xl">You Lose!</div>}
        <Image src="/rotate-right.svg" width={20} height={20} alt="replay" className="absolute right-0 top-0 cursor-pointer" priority onClick={() => restart()} />
      </div>
      <div className="flex items-center justify-center">
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(0, 0)}>{grid[0][0]}</div>
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(0, 1)}>{grid[0][1]}</div>
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(0, 2)}>{grid[0][2]}</div>
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(1, 0)}>{grid[1][0]}</div>
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(1, 1)}>{grid[1][1]}</div>
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(1, 2)}>{grid[1][2]}</div>
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(2, 0)}>{grid[2][0]}</div>
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(2, 1)}>{grid[2][1]}</div>
          <div className="bg-neutral-400 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(2, 2)}>{grid[2][2]}</div>
        </div>
      </div>
    </div>
  );
}

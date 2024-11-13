"use client"

import { useEffect, useState } from "react";

export default function Home() {
  const [win, setWin] = useState<string | null>(null);
  const [algorithm, setAlgorithm] = useState<string>("random");
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
    if (checkWin(newGrid) || checkTie(newGrid)) return;
    
    const response = await fetch(process.env.NEXT_PUBLIC_API as string, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ grid: newGrid, algorithm: algorithm })
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

  const checkTie = (grid: string[][]) => {
    if (grid.every(row => row.every(cell => cell !== " "))) {
      setWin("tie")
      return true;
    }
    return false;
  };

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
        {win === "tie" && <div className="font-bold text-2xl">It was a tie!</div>}
        <div className="absolute right-0 top-0 cursor-pointer text-foreground size-8" onClick={() => restart()}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor">
            <path d="M463.5 224l8.5 0c13.3 0 24-10.7 24-24l0-128c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1c-87.5 87.5-87.5 229.3 0 316.8s229.3 87.5 316.8 0c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0c-62.5 62.5-163.8 62.5-226.3 0s-62.5-163.8 0-226.3c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8l119.5 0z"/>
          </svg>
        </div>
      </div>
      <div className="flex items-center justify-center">
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(0, 0)}>{grid[0][0]}</div>
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(0, 1)}>{grid[0][1]}</div>
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(0, 2)}>{grid[0][2]}</div>
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(1, 0)}>{grid[1][0]}</div>
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(1, 1)}>{grid[1][1]}</div>
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(1, 2)}>{grid[1][2]}</div>
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(2, 0)}>{grid[2][0]}</div>
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(2, 1)}>{grid[2][1]}</div>
          <div className="bg-neutral-500 size-64 grid place-items-center font-extrabold text-9xl" onClick={() => placeSquare(2, 2)}>{grid[2][2]}</div>
        </div>
      </div>
      <div className="mt-2 flex gap-4 text-xl text-background font-bold">
        <div className={`bg-neutral-500 px-4 py-2 rounded-full border-2 border-neutral-700 dark:border-neutral-300 ${ algorithm === "random" ? "underline" : "" }`} onClick={() => setAlgorithm("random")}>Random</div>
        <div className={`bg-neutral-500 px-4 py-2 rounded-full border-2 border-neutral-700 dark:border-neutral-300 ${ algorithm === "heuristic" ? "underline" : "" }`} onClick={() => setAlgorithm("heuristic")}>Heuristic</div>
        <div className={`bg-neutral-500 px-4 py-2 rounded-full border-2 border-neutral-700 dark:border-neutral-300 ${ algorithm === "minimax" ? "underline" : "" }`} onClick={() => setAlgorithm("minimax")}>Minimax</div>
        <div className={`bg-neutral-500 px-4 py-2 rounded-full border-2 border-neutral-700 dark:border-neutral-300 ${ algorithm === "abp_minimax" ? "underline" : "" }`} onClick={() => setAlgorithm("abp_minimax")}>Minimax (ABP)</div>
      </div>
    </div>
  );
}

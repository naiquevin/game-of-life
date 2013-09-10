(ns ^{:doc "Helper for parsing .cells files"
      :author "Vineet Naik <naikvin@gmail.com"}
  gol-clj.cells
  (:require [clojure.java.io :as io]))


(defn get-lines
  "Reads lines from a file with name `file-name`"
  [file-name]
  (line-seq (io/reader file-name)))


(defn get-name
  "Extracts name of the cell pattern from lines of .cells file"
  [lines]
  (second (first (re-seq #"!Name: (.+)" (first lines)))))


(defn cell-char? 
  "Checks whether a character is a valid cell char"
  [c] (or (= c \.) (= c \O)))


(defn chars->symbs
  "Converts cell chars to symbols representing cell states"
  [chars]
  (mapv (fn [c] (if (= c \O) :alive :dead)) chars))


(defn get-cells
  "Gets a nested vector representing the cells"
  [lines]
  (mapv
   (comp chars->symbs (partial filter cell-char?))
   (filter (comp cell-char? first) lines)))


(defn num-rows
  "Gets the number of rows in the cell grid"
  [cells]
  (count cells))


(defn num-cols
  "Gets the number of columns in the cell grid"
  [cells]
  (count (first cells)))


(defn pad-cells
  "Pads the grid with two blank rows and columns on either sides"
  [cells]
  (letfn [(pad-cols [cells]
            (mapv (fn [row] (vec (concat [:dead :dead] row [:dead :dead]))) cells))
          (pad-rows [cells]
            (let [blank-row (vec (repeat (num-cols cells) :dead))]
              (vec (concat [blank-row blank-row] cells [blank-row blank-row]))))]
    (pad-rows (pad-cols cells))))


(defn grid
  "Loads the grid map by reading the .cells file"
  [file-name]
  (let [lines (get-lines file-name)]
    {:name (get-name lines)
     :cells (get-cells lines)}))


(defn surr-cell-idxs
  "Gets surrounding cell indexes of the given cell in grid"
  [[row col] cells]
  (let [nr (num-rows cells)
        nc (num-cols cells)]
    (filter (fn [[r c]]
              (and (>= r 0) (>= c 0) (< r nr) (< c nc)))
            [[(- row 1) (- col 1)]
             [(- row 1)    col   ]
             [(- row 1) (+ col 1)]
             [   row    (- col 1)]
             [   row    (+ col 1)]
             [(+ row 1) (- col 1)]
             [(+ row 1)    col   ]
             [(+ row 1) (+ col 1)]])))


(defn get-cell
  "Gets the value of a cell by it's index (position in matrix)"
  [[row col] cells]
  (nth (nth cells row) col))


(defn count-neighbours
  "Gets the no. of surrounding cells that are alive"
  [pos cells]
  (count
   (filter (fn [c] (= c :alive))
           (map (fn [p] (get-cell p cells))
                (surr-cell-idxs pos cells)))))


(defn indexed-cells
  "Gets cells where paired with their positions"
  [cells]
  (vec
   (map-indexed
    (fn [i x]
      (vec (map-indexed (fn [j y] [[i j] y]) x)))
    cells)))


(ns gol-clj.cells-test
  (:require [clojure.test :refer :all]
            [gol-clj.core :refer :all]
            [gol-clj.cells :refer :all]))


(def C1 [[:dead :dead :dead :dead :dead]
         [:dead :dead :dead :dead :dead]
         [:dead :dead :dead :dead :dead]
         [:dead :dead :dead :dead :dead]])

(def C2 [[:dead :dead :alive]
         [:alive :dead :dead]
         [:dead :alive :dead]
         [:dead :dead :alive]])

(def C3 [[:dead :dead :dead :dead :dead :dead]
         [:dead :dead :alive :alive :alive :dead]
         [:dead :alive :alive :alive :dead :dead]
         [:dead :dead :dead :dead :dead :dead]])

(def C4 [[:dead :dead :dead :alive :dead :dead]
         [:dead :alive :dead :dead :alive :dead]
         [:dead :alive :dead :dead :alive :dead]
         [:dead :dead :alive :dead :dead :dead]])


(deftest cell-char-test
  (testing "cell-char? function"
    (is (cell-char? \.))
    (is (cell-char? \O))
    (is (not (cell-char? \x)))))


(deftest chars->symbs-test
  (testing "chars->symbs function"
    (is (= (chars->symbs [\. \. \O \. \O]))
        [:dead :dead :alive :dead :alive])))


(deftest num-rows-test
  (testing "num-rows function"
    (is (= (num-rows C1) 4))))


(deftest num-cols-test
  (testing "num-cols function"
    (is (= (num-cols C1) 5))))


(deftest pad-cells-test
  (testing "pad-cells function"
    (let [padded (pad-cells C1 2)
          padded-row (vec (concat [:dead :dead] (first C1) [:dead :dead]))]
      (is (= (num-cols padded) (+ (* 2 2) (num-cols C1))))
      (is (= (num-rows padded) (+ (* 2 2) (num-rows C1))))
      (is (= (first padded) padded-row))
      (is (= (second padded) padded-row))
      (is (= (last padded) padded-row))
      (is (= (last (butlast padded)) padded-row)))))


(deftest surr-cell-idxs-test
  (testing "surr-cell-idxs function"
    (are [x y] (= (sort (surr-cell-idxs x C1)) (sort y))
         [0 0] [[0 1] [1 0] [1 1]]
         [1 0] [[0 0] [2 0] [0 1] [1 1] [2 1]]
         [1 1] [[0 0] [1 0] [2 0] [0 1] [2 1] [0 2] [1 2] [2 2]]
         [3 3] [[2 2] [2 3] [2 4] [3 2] [3 4]]
         [3 4] [[2 3] [2 4] [3 3]])))


(deftest get-cell-test
  (testing "get-cell function"
    (is (= (get-cell [0 0] C2) :dead))
    (is (= (get-cell [1 0] C2) :alive))
    (is (= (get-cell [3 2] C2) :alive))))


(deftest count-neighbours-test
  (testing "count-neighbours function"
    (is (= (count-neighbours [1 0] C2)) 1)
    (is (= (count-neighbours [0 2] C2)) 0)
    (is (= (count-neighbours [1 1] C3)) 3)))

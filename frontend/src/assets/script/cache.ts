import type { AxiosRequestConfig } from "axios";
import axios from "axios";

type Cache = {
  expiration: number;
  data: any;
}

const cache: { [key: string]: Cache } = {};

function getCache(key: string): any | undefined {
  if (key in cache) return cache[key].data;
}

function setCache(key: string, data: any, expiration: number): void {
  cache[key] = { expiration: Date.now() + expiration * 1000, data };
}

function existsCache(key: string): boolean {
  if (key in cache) {
    if (cache[key].expiration > Date.now()) return true;
    else delete cache[key];
  }
  return false;
}

export function getWithCache(url: string, expiration?: number, config?: AxiosRequestConfig) : Promise<any> {
  if (existsCache(url)) return Promise.resolve(getCache(url));
  else return new Promise((resolve, reject) => {
    axios.get(url, config).then((res) => {
      setCache(url, res, expiration ?? 120);
      resolve(res);
    }).catch(reject);
  });
}

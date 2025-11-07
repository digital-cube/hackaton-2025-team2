declare module 'openrouteservice-js' {
  export default class Openrouteservice {
    static Directions: new (config: { api_key: string }) => any;
  }
}
